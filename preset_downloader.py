import os
import struct

preset_folder_path = 'Massive_Factory_Preset'
parameters_list = []

for filename  in os.listdir(preset_folder_path):
    if filename.endswith('.nmsv'):
        file_path = os.path.join(preset_folder_path, filename)
        with open(file_path,'rb')as f:
            data= f.read()
            first_byte=data[0]
            print(filename,hex(first_byte))
            if data[0] == 0x49 and data[1] == 0x49:
                # ファイルヘッダーが'II'の場合の処理
                print('if data[0] == 0x49 and data[1] == 0x49:')
            elif data[0] == 0x4D and data[1] == 0x4D:
                print('elif data[0] == 0x4D and data[1] == 0x4D:')
                # ファイルヘッダーが'MM'の場合の処理
            else:
                print('else data')
        # その他の場合の処理
        # バイトオーダーマークがない場合の判別方法
        with open(file_path, 'rb') as f:
            bytes = f.read()
            print('hello')
            if bytes[0] == 0x47:  # 特定のバイト値を見る
                print('ファイル形式: MPEG-2 (バイトオーダーマークなし)')
            elif bytes[0] == 0x41:  # 他の特定のバイト値を見る
                print('ファイル形式: Apple QuickTime (バイトオーダーマークなし)')
                if len(data)<8:
                    print('hello2')
                    print(f"Error:Invalid file format.")
                    continue            
        metadata_length = struct.unpack('>i',data[:4])[0]
        if metadata_length<0:
            metadata_length=0
        elif metadata_length>len(data)-4:
            metadata_length=len(data)-4
        if len(data)<metadata_length+8:
            print(f"Error")
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
                    offset +=   4         

                elif data_type == b'i16 ':
                    value = struct.unpack('>h', data[offset:offset+2])[0]
                    offset += 2
                elif data_type == b'i8  ':
                    value = struct.unpack('>b', data[offset:offset+1])[0]
                    offset += 1
                elif data_type == b'bool':
                    value = bool(struct.unpack('>i', data[offset:offset+4])[0])
                    offset += 4
                elif data_type == b'txt ':
                    value_length = struct.unpack('>i', data[offset:offset+4])[0]
                    offset += 4
                    if value_length > len(data) - offset:
                        print(f"Error: Invalid file format ({filename})")
                        break
                    value = data[offset-value_length:offset].decode('utf-8')
                    offset += value_length

                elif data_type == b'b   ':
                    value_length = struct.unpack('>i', data[offset:offset+4])[0]
                    offset += 4
                    if value_length > len(data) - offset:
                        print(f"Error: Invalid file format ({filename})")
                        break
                    # バイト列として値を読み取る
                    value = data[offset:offset+value_length]
                    offset += value_length    
                else:
                    print(f"Error: Invalid data type ({data_type}) for parameter '{param_name}' in preset '{preset_name}'")
                    break

                parameters[param_name] = value

        parameters_list.append((preset_name, parameters))
        
