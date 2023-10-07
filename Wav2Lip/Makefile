DATA_DIR=/home/yt/Raven/backend/data

inf:
	python3 ./inference.py \
		--checkpoint_path /home/yt/Raven/backend/Wav2Lip/checkpoints/wav2lip.pth \
		--face ${DATA_DIR}/input.mp4 \
		--audio ${DATA_DIR}/temp.mp3 \
		--outfile ${DATA_DIR}/output.mp4 \
		--face_det_batch_size 64 \
		--wav2lip_batch_size 256