AI-Powered E-commerce Backend

This project is a backend system for an e-commerce platform enhanced with AI-driven product search and recommendations. It combines traditional backend development with modern multimodal retrieval techniques.

Overview

The system allows users to browse, search, and purchase products while enabling sellers to upload new items. Each product is processed by an ML pipeline that generates semantic embeddings, making it possible to perform image-based and text-based search.

The core idea is to move beyond keyword search and enable semantic understanding of products using vision-language models.

Features
User authentication with access and refresh tokens
Product upload with image storage via Cloudinary
Order management with relational data modeling
Background worker for asynchronous ML processing
Automatic caption generation using a fine-tuned BLIP model
Image and text embeddings using CLIP
Fast similarity search using FAISS
Multimodal search:
text → product retrieval
image → similar product retrieval
Architecture

The system is divided into two main components:

1. API Backend

Built with FastAPI and SQLAlchemy (async), it handles:

authentication
product and order management
file uploads
API responses and error handling
2. ML Service

A background worker continuously processes new products:

generates captions from images
computes embeddings
indexes them into FAISS for retrieval

Products are initially marked as PENDING, then move to PROCESSING, and finally READY once indexed.

Search Pipeline
User provides a text query or an image
CLIP encodes the query into a vector
FAISS performs nearest neighbor search
Matching product IDs are returned
Metadata is fetched from the database

This enables semantic search across a large product catalog.

Tech Stack
FastAPI
PostgreSQL
SQLAlchemy (async ORM)
PyTorch
CLIP (OpenAI)
BLIP (fine-tuned for fashion captions)
FAISS
Cloudinary
Notes

This project is intended for learning and demonstration purposes.
The dataset used for indexing is based on a large-scale fashion dataset and is not used commercially.
