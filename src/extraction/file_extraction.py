''''
Here we start trying a docling object parsing
and serialize, so that the chunks we get
has serialized artifact object.
'''

import json
import logging
import os
import time
from pathlib import Path
from typing import Iterable, Optional
from docling_core.transforms.chunker.base import BaseChunk
from docling_core.transforms.chunker.hierarchical_chunker import DocChunk
from docling_core.types.doc.labels import DocItemLabel
from rich.console import Console
from rich.panel import Panel
from docling_core.transforms.chunker.tokenizer.base import BaseTokenizer
from docling_core.transforms.chunker.tokenizer.huggingface import HuggingFaceTokenizer
from transformers import AutoTokenizer
from docling_core.transforms.chunker.hybrid_chunker import HybridChunker
from docling_core.types import DoclingDocument
from dotenv import load_dotenv

load_dotenv()
from docling_core.types.doc import ImageRefMode
from docling.backend.docling_parse_v4_backend import DoclingParseV4DocumentBackend
from docling.datamodel.base_models import ConversionStatus, InputFormat
from docling.datamodel.document import ConversionResult
from docling.datamodel.pipeline_options import PdfPipelineOptions
from docling.document_converter import DocumentConverter, PdfFormatOption

_log = logging.getLogger(__name__)

# Export toggles:
# - USE_V2 controls modern Docling document exports.
# - USE_LEGACY enables legacy Deep Search exports for comparison or migration.
USE_V2 = True
USE_LEGACY = False


def export_documents(
    conv_results: Iterable[ConversionResult],
    output_dir: Path,
):
    output_dir.mkdir(parents=True, exist_ok=True)

    success_count = 0
    failure_count = 0
    partial_success_count = 0

    for conv_res in conv_results:
        if conv_res.status == ConversionStatus.SUCCESS:
            success_count += 1
            doc_filename = conv_res.input.file.stem

            if USE_V2:
                # Recommended modern Docling exports. These helpers mirror the
                # lower-level "export_to_*" methods used below, but handle
                # common details like image handling.
                conv_res.document.save_as_json(
                    output_dir / f"{doc_filename}.json",
                    image_mode=ImageRefMode.PLACEHOLDER,
                )
                # conv_res.document.save_as_html(
                #     output_dir / f"{doc_filename}.html",
                #     image_mode=ImageRefMode.EMBEDDED,
                # )
                # conv_res.document.save_as_document_tokens(
                #     output_dir / f"{doc_filename}.doctags.txt"
                # )
                # conv_res.document.save_as_markdown(
                #     output_dir / f"{doc_filename}.md",
                #     image_mode=ImageRefMode.PLACEHOLDER,
                # )
                # conv_res.document.save_as_markdown(
                #     output_dir / f"{doc_filename}.txt",
                #     image_mode=ImageRefMode.PLACEHOLDER,
                #     strict_text=True,
                # )
                #
                # # Export Docling document format to YAML:
                # with (output_dir / f"{doc_filename}.yaml").open("w") as fp:
                #     fp.write(yaml.safe_dump(conv_res.document.export_to_dict()))
                #
                # # Export Docling document format to doctags:
                # with (output_dir / f"{doc_filename}.doctags.txt").open("w") as fp:
                #     fp.write(conv_res.document.export_to_document_tokens())
                #
                # # Export Docling document format to markdown:
                # with (output_dir / f"{doc_filename}.md").open("w") as fp:
                #     fp.write(conv_res.document.export_to_markdown())
                #
                # # Export Docling document format to text:
                # with (output_dir / f"{doc_filename}.txt").open("w") as fp:
                #     fp.write(conv_res.document.export_to_markdown(strict_text=True))

            if USE_LEGACY:
                # Export Deep Search document JSON format:
                with (output_dir / f"{doc_filename}.legacy.json").open(
                    "w", encoding="utf-8"
                ) as fp:
                    fp.write(json.dumps(conv_res.legacy_document.export_to_dict()))

                # Export Text format:
                with (output_dir / f"{doc_filename}.legacy.txt").open(
                    "w", encoding="utf-8"
                ) as fp:
                    fp.write(
                        conv_res.legacy_document.export_to_markdown(strict_text=True)
                    )

                # Export Markdown format:
                with (output_dir / f"{doc_filename}.legacy.md").open(
                    "w", encoding="utf-8"
                ) as fp:
                    fp.write(conv_res.legacy_document.export_to_markdown())

                # Export Document Tags format:
                with (output_dir / f"{doc_filename}.legacy.doctags.txt").open(
                    "w", encoding="utf-8"
                ) as fp:
                    fp.write(conv_res.legacy_document.export_to_document_tokens())

        elif conv_res.status == ConversionStatus.PARTIAL_SUCCESS:
            _log.info(
                f"Document {conv_res.input.file} was partially converted with the following errors:"
            )
            for item in conv_res.errors:
                _log.info(f"\t{item.error_message}")
            partial_success_count += 1
        else:
            _log.info(f"Document {conv_res.input.file} failed to convert.")
            failure_count += 1

    _log.info(
        f"Processed {success_count + partial_success_count + failure_count} docs, "
        f"of which {failure_count} failed "
        f"and {partial_success_count} were partially converted."
    )
    return success_count, partial_success_count, failure_count


def batch_file_extraction(data_folder, input_doc_paths):
    # buf = BytesIO((data_folder / "pdf/2206.01062.pdf").open("rb").read())
    # docs = [DocumentStream(name="my_doc.pdf", stream=buf)]
    # input = DocumentConversionInput.from_streams(docs)

    # # Turn on inline debug visualizations:
    # settings.debug.visualize_layout = True
    # settings.debug.visualize_ocr = True
    # settings.debug.visualize_tables = True
    # settings.debug.visualize_cells = True

    # Configure the PDF pipeline. Enabling page image generation improves HTML
    # previews (embedded images) but adds processing time.


    pipeline_options = PdfPipelineOptions()
    pipeline_options.generate_page_images = True

    doc_converter = DocumentConverter(
        format_options={
            InputFormat.PDF: PdfFormatOption(
                pipeline_options=pipeline_options, backend=DoclingParseV4DocumentBackend
            )
        }
    )

    start_time = time.time()

    # Convert all inputs. Set `raises_on_error=False` to keep processing other
    # files even if one fails; errors are summarized after the run.
    conv_results = doc_converter.convert_all(
        input_doc_paths,
        raises_on_error=False,  # to let conversion run through all and examine results at the end
    )
    # Write outputs to ./scratch and log a summary.
    _success_count, _partial_success_count, failure_count = export_documents(
        conv_results, output_dir=Path(f"{data_folder}/extracted_data/")
    )

    end_time = time.time() - start_time

    _log.info(f"Document conversion complete in {end_time:.2f} seconds.")

    if failure_count > 0:
        raise RuntimeError(
            f"The example failed converting {failure_count} on {len(input_doc_paths)}."
        )



def find_n_th_chunk_with_label(
    iter: Iterable[BaseChunk], n: int, label: DocItemLabel
) -> Optional[DocChunk]:
    num_found = -1
    for i, chunk in enumerate(iter):
        doc_chunk = DocChunk.model_validate(chunk)
        for it in doc_chunk.meta.doc_items:
            if it.label == label:
                num_found += 1
                if num_found == n:
                    return i, chunk
    return None, None


def print_chunk(chunks, chunk_pos, chunker, tokenizer, console):
    chunk = chunks[chunk_pos]
    ctx_text = chunker.contextualize(chunk=chunk)
    num_tokens = tokenizer.count_tokens(text=ctx_text)
    doc_items_refs = [it.self_ref for it in chunk.meta.doc_items]
    title = f"{chunk_pos=} {num_tokens=} {doc_items_refs=}"
    console.print(Panel(ctx_text, title=title))



def chunking_dl_doc_with_artifacts(chunker, tokenizer, dldoc, console):
    chunk_iter = chunker.chunk(dl_doc=dldoc)
    chunks = list(chunk_iter)
    print(f"chunks: {chunks}")
    i, chunk = find_n_th_chunk_with_label(chunks, n=0, label=DocItemLabel.TABLE)
    print_chunk(
        chunks=chunks,
        chunk_pos=i,
        chunker = chunker,
        tokenizer = tokenizer,
        console = console
    )


def chunking_docfile(dldoc):
    '''
    given a dldoc it chunks it and prints the chunks.
    :param dldoc:
    :return: return chunks in a list.
    '''


    chunker = HybridChunker()
    chunk_iter = chunker.chunk(dl_doc=dldoc)

    for i, chunk in enumerate(chunk_iter):
        print(f"=== {i} ===")
        # print(f"chunk.text:\n{f'{chunk.text[:300]}…'!r}")
        print(f"chunk_text: {chunk.text}")

        enriched_text = chunker.contextualize(chunk=chunk)
        print(f"enriched_text: {enriched_text}")
        # print(f"chunker.contextualize(chunk):\n{f'{enriched_text[:300]}…'!r}")

        print()


def test():
    logging.basicConfig(level=logging.INFO)
    console = Console(
        width=200,  # for getting Markdown tables rendered nicely
    )

    # Location of sample PDFs used by this example. If your checkout does not
    # include test data, change `data_folder` or point `input_doc_paths` to
    # your own files.

    data_folder = os.environ["DATA_ROOT"]

    input_doc_paths = [
        f"{data_folder}/raw_data/pdfs/2023_UCR_Manual_EN_final.pdf",
        f"{data_folder}/raw_data/pdfs/Homicide_KG.pdf",
        f"{data_folder}/raw_data/pdfs/nihms-362971-trunc.pdf",
        f"{data_folder}/raw_data/docs/Company_QuantumNext_Systems.docx"
    ]

    # batch_file_extraction(data_folder, input_doc_paths)

    # file_path = data_folder + "/extracted_data/2023_UCR_Manual_EN_final.json"

    file_path = data_folder + "/extracted_data/Homicide_KG.json"

    with open(file_path, "r") as fp:
        doc_dict = json.loads(fp.read())

    # Recreate the DoclingDocument object
    dldoc = DoclingDocument.model_validate(doc_dict)

    # You can now work with the 'doc' object, for example, export to Markdown
    print(dldoc.export_to_markdown())


    EMBED_MODEL_ID = "sentence-transformers/all-MiniLM-L6-v2"

    tokenizer: BaseTokenizer = HuggingFaceTokenizer(
        tokenizer=AutoTokenizer.from_pretrained(EMBED_MODEL_ID),
    )
    chunker = HybridChunker(tokenizer=tokenizer)
    chunking_dl_doc_with_artifacts(chunker, tokenizer, dldoc, console)

    #chunking_docfile(dldoc)


if __name__ == "__main__":
    test()