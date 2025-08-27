# javis.py
# 시스템 마이크를 사용하여 음성을 녹음하고, 텍스트로 변환하여 저장하는 스크립트

import pyaudio
import wave
import os
from datetime import datetime
import speech_recognition as sr
import glob
import csv

class AudioRecorder:
    """
    마이크로부터 오디오를 녹음하고 WAV 파일로 저장하는 클래스.
    """
    def __init__(self):
        # 녹음 관련 설정
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 44100
        self.CHUNK = 1024
        self.RECORD_SECONDS = 5
        self.OUTPUT_DIR = "records"

    def record_audio(self):
        """
        마이크 입력을 받아 지정된 시간 동안 녹음하고 파일로 저장합니다.
        """
        audio = pyaudio.PyAudio()
        print("="*40)
        print(f"음성 녹음을 시작합니다. ({self.RECORD_SECONDS}초간 녹음)")
        print("="*40)

        stream = audio.open(format=self.FORMAT, channels=self.CHANNELS,
                            rate=self.RATE, input=True,
                            frames_per_buffer=self.CHUNK)
        frames = []
        for _ in range(0, int(self.RATE / self.CHUNK * self.RECORD_SECONDS)):
            data = stream.read(self.CHUNK)
            frames.append(data)

        print("...녹음이 완료되었습니다.")
        stream.stop_stream()
        stream.close()
        audio.terminate()
        self.save_to_file(frames, audio)

    def save_to_file(self, frames, audio_instance):
        """
        녹음된 오디오 프레임들을 WAV 파일로 저장합니다.
        """
        if not os.path.exists(self.OUTPUT_DIR):
            os.makedirs(self.OUTPUT_DIR)
            print(f"'{self.OUTPUT_DIR}' 폴더를 생성했습니다.")

        now = datetime.now()
        filename = now.strftime('%Y%m%d-%H%M%S') + '.wav'
        filepath = os.path.join(self.OUTPUT_DIR, filename)

        with wave.open(filepath, 'wb') as wf:
            wf.setnchannels(self.CHANNELS)
            wf.setsampwidth(audio_instance.get_sample_size(self.FORMAT))
            wf.setframerate(self.RATE)
            wf.writeframes(b''.join(frames))
        
        print(f"✅ 녹음 파일이 '{filepath}' 경로에 저장되었습니다.")
        print("="*40)


class Transcriber:
    """
    WAV 오디오 파일을 텍스트로 변환하고 CSV로 저장하는 클래스.
    """
    def __init__(self, audio_dir="records"):
        self.recognizer = sr.Recognizer()
        self.audio_dir = audio_dir

    def transcribe_all_files(self):
        """
        지정된 폴더의 모든 WAV 파일을 텍스트로 변환합니다.
        """
        # records 폴더의 모든 .wav 파일 목록을 가져옴
        wav_files = glob.glob(os.path.join(self.audio_dir, '*.wav'))
        
        if not wav_files:
            print("변환할 음성 파일이 'records' 폴더에 없습니다.")
            return

        print("\n" + "="*40)
        print("음성 파일 텍스트 변환을 시작합니다.")
        print("="*40)

        for wav_path in wav_files:
            print(f"-> 파일 변환 중: {os.path.basename(wav_path)}")
            try:
                with sr.AudioFile(wav_path) as source:
                    # 오디오 파일의 데이터를 읽음
                    audio_data = self.recognizer.record(source)
                
                # Google Web Speech API를 사용하여 텍스트로 변환 (한국어 설정)
                text = self.recognizer.recognize_google(audio_data, language='ko-KR')
                print(f"   인식된 텍스트: {text}")
                self.save_to_csv(wav_path, text)

            except sr.UnknownValueError:
                print("   [오류] 음성을 인식할 수 없습니다.")
            except sr.RequestError as e:
                print(f"   [오류] Google API 요청에 실패했습니다; {e}")
            except Exception as e:
                print(f"   [오류] 파일 처리 중 에러 발생: {e}")

        print("\n" + "="*40)
        print("모든 음성 파일의 텍스트 변환이 완료되었습니다.")
        print("="*40)

    def save_to_csv(self, wav_path, text):
        """
        인식된 텍스트를 CSV 파일로 저장합니다.
        """
        # .wav 확장자를 .csv로 변경하여 파일 경로 생성
        csv_path = os.path.splitext(wav_path)[0] + '.csv'
        
        with open(csv_path, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.writer(f)
            # 헤더 작성
            writer.writerow(['Time', 'Text'])
            # 내용 작성 (음성 파일 시작 시간을 0으로 표기)
            writer.writerow(['0', text])
        
        print(f"   -> 결과가 '{os.path.basename(csv_path)}' 파일에 저장되었습니다.")


if __name__ == '__main__':
    # 1. 음성 녹음 실행
    recorder = AudioRecorder()
    recorder.record_audio()

    # 2. 녹음된 모든 파일들을 텍스트로 변환
    transcriber = Transcriber()
    transcriber.transcribe_all_files()
