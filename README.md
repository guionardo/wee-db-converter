# wee-db-converter
Converter service from MariaDB to MongoDB

[![CodeQL](https://github.com/guionardo/wee-db-converter/actions/workflows/codeql-analysis.yml/badge.svg)](https://github.com/guionardo/wee-db-converter/actions/workflows/codeql-analysis.yml)
[![Pylint](https://github.com/guionardo/wee-db-converter/actions/workflows/pylint.yml/badge.svg)](https://github.com/guionardo/wee-db-converter/actions/workflows/pylint.yml)
[![wakatime](https://wakatime.com/badge/user/fb959963-d330-46bd-9113-448fe495af90/project/27ef23a4-1758-4d23-9de5-d5c3b81cc45c.svg)](https://wakatime.com/badge/user/fb959963-d330-46bd-9113-448fe495af90/project/27ef23a4-1758-4d23-9de5-d5c3b81cc45c)

## Tabelas

posts (usar post_types vazios, video, media, link, photo)

FK dependem do valor de post_type

posts_photos
posts_links
posts_media (apenas source_provider YouTube)
posts_videos

## Exemplos

[Pasta](docs/samples)