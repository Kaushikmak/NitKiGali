from channels.generic.websocket import WebsocketConsumer
import json
from logservice import LogService
import sys

class WSConsumer(WebsocketConsumer):

    def connect(self):
        self.log = LogService(prefix="Websocket")
        self.log.write("--- Connection attempt started ---", "DEBUG")
        
        try:
            self.log.write("Attempting to accept connection...", "DEBUG")
            self.accept()
            self.log.write("Connection ACCEPTED", "INFO")

            self.log.write("Sending 'connected' confirmation message...", "DEBUG")
            self.send(text_data=json.dumps({"message": "connected"}))
            self.log.write("'connected' message sent.", "DEBUG")

            self.log.write("--- Connection successfully established ---", "INFO")

        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = exc_tb.tb_frame.f_code.co_filename
            line_num = exc_tb.tb_lineno
            
            error_msg = f"Websocket FAILED to connect: {e} [Type: {exc_type}, File: {fname}, Line: {line_num}]"
            self.log.write(error_msg, "ERROR")

            try:
                self.send(text_data=json.dumps({"ERROR": "Connection failed during handshake"}))
            except Exception:
                pass
            
            self.close()

    def receive(self, text_data=None, bytes_data=None):
        self.log.write("--- Message received ---", "DEBUG")
        
        if bytes_data:
            self.log.write(f"Received BYTES data: {len(bytes_data)} bytes", "INFO")

            self.log.write("Binary data not handled in this consumer.", "WARNING")
            self.send_json({"error": "Binary data is not supported"})
            return

        self.log.write(f"Received TEXT data: {text_data}", "INFO")
        
        try:
            self.log.write("Attempting to parse JSON...", "DEBUG")
            data = json.loads(text_data)
            self.log.write(f"JSON parsed successfully: {data}", "DEBUG")

            if "message" not in data:
                self.log.write(f"Received data missing 'message' key: {data}", "WARNING")
                self.send_json({"error": "Invalid data format. 'message' key is required."})
                return
                
            msg = data.get("message", "")
            self.log.write(f"Extracted message: '{msg}'", "DEBUG")

            response_msg = f"Echo: {msg}"
            self.log.write(f"Preparing to send echo response: '{response_msg}'", "DEBUG")
            
            self.send_json({"message": response_msg})
            
            self.log.write(f"Successfully sent echo response for: '{msg}'", "INFO")

        except json.JSONDecodeError as e:
            self.log.write(f"Failed to decode JSON: {e}", "ERROR")
            self.send_json({"error": "Invalid JSON format received."})
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = exc_tb.tb_frame.f_code.co_filename
            line_num = exc_tb.tb_lineno
            error_msg = f"Error in receive(): {e} [Type: {exc_type}, File: {fname}, Line: {line_num}]"
            
            self.log.write(error_msg, "ERROR")
            self.send_json({"error": "An internal server error occurred"})

    def disconnect(self, close_code):
        self.log.write(f"--- Disconnect initiated (Code: {close_code}) ---", "INFO")
        
        try:
            pass
        except Exception as e:
            self.log.write(f"Error during disconnect cleanup: {e}", "ERROR")
        finally:

            self.log.write("Closing logger...", "DEBUG")
            self.log.close()
            self.log.write("--- Connection fully closed ---", "INFO") 

    def send_json(self, data):
        try:
            self.log.write(f"Attempting to send JSON: {data}", "DEBUG")
            json_text = json.dumps(data)
            self.send(text_data=json_text)
            self.log.write("JSON message sent successfully.", "DEBUG")
        except Exception as e:
            self.log.write(f"Failed to send JSON message: {e}", "ERROR")