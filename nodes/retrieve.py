# import os
# import pandas as pd
# from langchain_community.document_loaders import (
#     PyPDFLoader, TextLoader, Docx2txtLoader, CSVLoader,
#     UnstructuredExcelLoader, UnstructuredPowerPointLoader,
#     UnstructuredHTMLLoader, UnstructuredMarkdownLoader, JSONLoader,
# )
# from langchain_text_splitters import RecursiveCharacterTextSplitter
# from langchain_community.vectorstores import Chroma
# from langchain_core.documents import Document
# from nodes.llm import embeddings
# from state import WorkflowState
# from logger import log

# RELEVANCE_THRESHOLD = 0.4
# CHROMA_PERSIST_DIR  = "./chroma_store"


# def load_file(file_path: str):
#     ext = os.path.splitext(file_path)[1].lower()

#     log("LOAD FILE", "Detecting file type", {
#         "extension": ext,
#         "file":      os.path.basename(file_path),
#     })

#     if ext == ".pdf":
#         return PyPDFLoader(file_path).load()
#     elif ext == ".docx":
#         return Docx2txtLoader(file_path).load()
#     elif ext in [".xlsx", ".xls"]:
#         return UnstructuredExcelLoader(file_path).load()
#     elif ext == ".csv":
#         df   = pd.read_csv(file_path)
#         text = df.to_string(index=False)
#         return [Document(page_content=text, metadata={"source": file_path})]
#     elif ext in [".pptx", ".ppt"]:
#         return UnstructuredPowerPointLoader(file_path).load()
#     elif ext in [".html", ".htm"]:
#         return UnstructuredHTMLLoader(file_path).load()
#     elif ext == ".md":
#         return UnstructuredMarkdownLoader(file_path).load()
#     elif ext == ".json":
#         return JSONLoader(
#             file_path=file_path,
#             jq_schema=".. | strings",
#             text_content=False,
#         ).load()
#     elif ext in [".py", ".js", ".ts", ".java", ".c", ".cpp", ".cs", ".go", ".rs", ".rb"]:
#         return TextLoader(file_path, encoding="utf-8").load()
#     else:
#         try:
#             return TextLoader(file_path, encoding="utf-8").load()
#         except Exception:
#             with open(file_path, "r", errors="ignore") as f:
#                 content = f.read()
#             return [Document(page_content=content, metadata={"source": file_path})]


# def retrieve(state: WorkflowState) -> dict:
#     file_path     = state["file_path"]
#     file_question = state["file_question"]
#     collection_name = "file_" + os.path.basename(file_path).replace(".", "_").replace(" ", "_")

#     log("RETRIEVE", "Checking ChromaDB for existing embeddings", {
#         "collection": collection_name,
#         "file_path":  file_path,
#     })

#     already_embedded = state.get("file_already_embedded", False)

#     if already_embedded:
#         log("RETRIEVE", "Reusing existing embeddings", {})
#         vectorstore = Chroma(
#             collection_name=collection_name,
#             embedding_function=embeddings,
#             persist_directory=CHROMA_PERSIST_DIR,
#         )
#     else:
#         documents = load_file(file_path)
#         splitter  = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
#         chunks    = splitter.split_documents(documents)

#         log("RETRIEVE", "File chunked", {"total_chunks": len(chunks)})

#         vectorstore = Chroma.from_documents(
#             documents=chunks,
#             embedding=embeddings,
#             collection_name=collection_name,
#             persist_directory=CHROMA_PERSIST_DIR,
#         )

#     results_with_scores = vectorstore.similarity_search_with_relevance_scores(file_question, k=6)

#     log("RETRIEVE", "Raw chunks retrieved", {
#         "total":  len(results_with_scores),
#         "scores": [round(score, 3) for _, score in results_with_scores],
#     })

#     filtered = [(doc, score) for doc, score in results_with_scores if score >= RELEVANCE_THRESHOLD]

#     if not filtered:
#         log("RETRIEVE WARN", "No chunks passed threshold — using top 3", {
#             "threshold": RELEVANCE_THRESHOLD,
#         })
#         filtered = results_with_scores[:3]

#     retrieved_chunks = "\n\n".join([doc.page_content for doc, _ in filtered])
#     retrieval_scores = [round(score, 3) for _, score in filtered]

#     log("RETRIEVE DONE", "Final chunks after relevance filter", {
#         "chunks_kept":      len(filtered),
#         "relevance_scores": retrieval_scores,
#         "preview":          retrieved_chunks[:200] + "...",
#     })

#     return {
#         "retrieved_chunks":      retrieved_chunks,
#         "retrieval_scores":      retrieval_scores,
#         "file_already_embedded": True,
#     }