#!/bin/bash
home_path=`cat ../project.yaml |shyaml get-value home_path`

python generate_passage_embeddings_harry.py \
	--passages ${home_path}'/data/harry_data.jsonl' \
	--output_dir ${home_path}'/embeddings' \
	--prefix '221020' \
	--model_name_or_path 'facebook/mcontriever' \
	--no_fp16 --lowercase --normalize_text

exit $?

