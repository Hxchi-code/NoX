    if mode == 'bug':
        # Kita gunakan -c:v libx264 untuk memastikan frame baru tersusun rapi
        # Ini akan sedikit lebih lambat, tapi dijamin file TIDAK AKAN CORRUPT
        subprocess.run(['ffmpeg', '-i', input_path, '-filter:v', 'setpts=5.0*PTS', '-c:v', 'libx264', '-crf', '23', '-preset', 'veryfast', '-c:a', 'copy', '-y', output_path], check=True)

