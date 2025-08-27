# javis.py
# 시스템 마이크를 사용하여 음성을 녹음하고 파일로 저장하는 스크립트

import pyaudio
import wave
import os
from datetime import datetime

class AudioRecorder:
    """
    마이크로부터 오디오를 녹음하고 WAV 파일로 저장하는 클래스.
    """
    def __init__(self):
        # 녹음 관련 설정
        self.FORMAT = pyaudio.paInt16  # 16비트 오디오 포맷
        self.CHANNELS = 1              # 모노 채널
        self.RATE = 44100              # 샘플링 레이트 (Hz)
        self.CHUNK = 1024              # 한 번에 읽어올 오디오 데이터의 프레임 수
        self.RECORD_SECONDS = 5        # 기본 녹음 시간 (초)
        self.OUTPUT_DIR = "records"    # 녹음 파일이 저장될 폴더

    def record_audio(self):
        """
        마이크 입력을 받아 지정된 시간 동안 녹음하고 파일로 저장합니다.
        """
        # PyAudio 객체 초기화
        audio = pyaudio.PyAudio()

        print("="*40)
        print("음성 녹음을 시작합니다. (5초간 녹음)")
        print("="*40)

        # 마이크 스트림 열기
        stream = audio.open(format=self.FORMAT,
                            channels=self.CHANNELS,
                            rate=self.RATE,
                            input=True,
                            frames_per_buffer=self.CHUNK)
        
        frames = []

        # 지정된 시간 동안 오디오 데이터 읽기
        for _ in range(0, int(self.RATE / self.CHUNK * self.RECORD_SECONDS)):
            data = stream.read(self.CHUNK)
            frames.append(data)

        print("...녹음이 완료되었습니다.")

        # 스트림 중지 및 닫기
        stream.stop_stream()
        stream.close()
        audio.terminate()

        # 녹음된 데이터를 파일로 저장
        self.save_to_file(frames, audio)

    def save_to_file(self, frames, audio_instance):
        """
        녹음된 오디오 프레임들을 WAV 파일로 저장합니다.
        """
        # 'records' 폴더가 없으면 생성
        if not os.path.exists(self.OUTPUT_DIR):
            os.makedirs(self.OUTPUT_DIR)
            print(f"'{self.OUTPUT_DIR}' 폴더를 생성했습니다.")

        # 파일 이름 생성 (년월일-시간분초.wav)
        now = datetime.now()
        filename = now.strftime('%Y%m%d-%H%M%S') + '.wav'
        filepath = os.path.join(self.OUTPUT_DIR, filename)

        # WAV 파일 쓰기
        with wave.open(filepath, 'wb') as wf:
            wf.setnchannels(self.CHANNELS)
            wf.setsampwidth(audio_instance.get_sample_size(self.FORMAT))
            wf.setframerate(self.RATE)
            wf.writeframes(b''.join(frames))
        
        print(f"✅ 녹음 파일이 '{filepath}' 경로에 저장되었습니다.")
        print("="*40)


if __name__ == '__main__':
    recorder = AudioRecorder()
    recorder.record_audio()
