from pydub import AudioSegment

class Audio:

    input_path: str
    audio_file: AudioSegment
    sample_rate: int
    output_path: str
    format: str
    
    def __init__(self, input_path):
        self.audio_file = AudioSegment.from_file(input_path)

    def convert_stereo_to_mono(self):
        """
        스테레오 오디오 파일을 모노로 변환하는 함수
            Args:
                input_file : 변환하고자 하는 AudioFile
            Logic: Mono로 변환된 오디오 객체
        """
        self.audio_file.set_channels(1)
        return

    def convert_sample_rate(self, sample_rate):
        """
        오디오 파일의 sample rate를 변환하는 함수
            Args:
                input_file : 변환하고자 하는 AudioFile
                sample_rate : 변환하고자 하는 Sample rate
            Logic: sample rate가 변환된 오디오 객체
        """
        self.audio_file.set_frame_rate(sample_rate)
        return 

    def export_wav(self, output_path, format):
        """
        오디오 파일을 Wav로 변환하는 함수
            Args:
                input_file : 변환하고자 하는 오디오 파일
                output_file : 변환된 오디오 파일 경로
            Logic: X, wav 파일 저장
        """
        self.audio_file.export(output_path, format) 
        return