# wee-db-converter
Converter service from MariaDB to MongoDB

[![CodeQL](https://github.com/guionardo/wee-db-converter/actions/workflows/codeql-analysis.yml/badge.svg)](https://github.com/guionardo/wee-db-converter/actions/workflows/codeql-analysis.yml)

## Tabelas

posts (usar post_types vazios, video, media, link, photo)

FK dependem do valor de post_type

posts_photos
posts_links
posts_media (apenas source_provider YouTube)
posts_videos
