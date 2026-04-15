from smbus2 import SMBus
import time

class i2c_master:
    def __init__(self,add,bus_num):
        self.slave_add = add 
        self.bus_num = bus_num

    def send_to_slave(self, cmd_byte):
        """
        スレーブを呼び出し、データを送信する関数
        address : スレーブの7ビットアドレス
        cmd_byte : 送信したい命令（センサー番号など）
        data_byte: 続けて送りたい値（任意）
        """
        try:
            with SMBus(self.bus_num) as bus:#よくわかってない
                bus.write_byte(self.slave_add, cmd_byte)
                
        except Exception as e:
            print(f"送信エラー: {e}")

def get_to_slave(self,sensor_id):
    try:
        with SMBus(self.bus_num) as bus:#よくわかってない
            return bus.read_byte_data(self.add, sensor_id)
                
    except Exception as e:
        print(f"送信エラー: {e}")
    

# --- 設定エリア ---
# 通信相手（Pico）のアドレス
# Raspberry Pi 4の標準I2Cバス番号（GPIO 2, 3を使用）
a = i2c_master(0x41,1)


# --- メイン処理 ---
if __name__ == "__main__":
    a.send_to_slave(0x1)#モーター
    
    time.sleep(5)

    result = a.get_to_slave(0x2)#湿り気
    print(result)