import os
import struct

preset_folder_path = 'Massive_Factory_Preset'  # プリセットファイルが保存されたフォルダのパス
parameters_list = []

for filename in os.listdir(preset_folder_path):
    if filename.endswith('.nmsv'):  # ファイルが.nmsv拡張子である場合
        file_path = os.path.join(preset_folder_path, filename)
        with open(file_path, 'rb') as f:
            data = f.read()

        if len(data) < 8:
            print(f"Error: Invalid file format ({filename})")
            continue

        metadata_length = struct.unpack('>i', data[:4])[0]
        metadata = data[4:4 + metadata_length]

        if len(data) < metadata_length + 8:
            print(f"Error: Invalid file format ({filename})")
            continue

        version, preset_name_length = struct.unpack('>ii', data[4 + metadata_length:4 + metadata_length + 8])
        preset_name = struct.unpack('>{}s'.format(preset_name_length), data[4 + metadata_length + 8:4 + metadata_length + 8 + preset_name_length])[0].decode('utf-8')

        parameters = {}
        offset = 4 + metadata_length + 8 + preset_name_length

        while offset < len(data):
            param_name_length, data_type = struct.unpack('>i4s', data[offset:offset+8])
            offset += 8
            param_name = data[offset:offset+param_name_length].decode('utf-8')
            offset += param_name_length
            if data_type == b'f32 ':
                value = struct.unpack('>f', data[offset:offset+4])[0]
                offset += 4
            elif data_type == b'i32 ':
                value = struct.unpack('>i', data[offset:offset+4])[0]
                offset += 4
            elif data_type == b'enu ':
                value_length = struct.unpack('>i', data[offset:offset+4])[0]
                value = data[offset+4:offset+4+value_length].decode('utf-8')
                offset += 4 + value_length
            else:
                raise ValueError(f'Unsupported data type: {data_type}')

                parameters[param_name] = value

            print(parameters_list)
