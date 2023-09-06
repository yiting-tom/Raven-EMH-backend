DATA_DIR=/home/yt/backend/data

inf:
	python3 ./inference.py \
		--checkpoint_path /home/yt/backend/Wav2Lip/checkpoints/wav2lip.pth \
		--face ${DATA_DIR}/avatar.png \
		--audio ${DATA_DIR}/demo-sound.mp3 \
		--outfile ${DATA_DIR}/output.mp4 \
		--face_det_batch_size 64 \
		--wav2lip_batch_size 256