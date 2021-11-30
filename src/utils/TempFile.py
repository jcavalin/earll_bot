import os


class TempFile:
    tmp_dir = 'tmp'
    tmp_files_created = []

    def download(self, message):
        self.create_tmp_dir()

        file = message.get_file()
        file_path = self.get_filepath(f'{message.file_unique_id}')
        file.download(file_path)

        return file_path

    def get_filepath(self, file_name):
        tmp_file_name = f'{self.tmp_dir}/{file_name}'
        self.tmp_files_created.append(tmp_file_name)

        return tmp_file_name

    def delete_tmp_files(self):
        for file in self.tmp_files_created:
            if not os.path.exists(file):
                continue
            os.remove(file)

    def create_tmp_dir(self):
        if not os.path.exists(self.tmp_dir):
            os.mkdir(self.tmp_dir)
