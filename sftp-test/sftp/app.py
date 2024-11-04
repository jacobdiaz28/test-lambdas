import paramiko
import base64
import hashlib

hostname = "test.acteln.com"
username = "ugrwtfpnrrcfwmjhqxhmrdyo"
password = "zZN90Euoyi6iJdH7m777xOkf"
file_path = "Downloads/test.txt"
## ssh-keyscan -H test.acteln.com | ssh-keygen -lf -
fingerprint_expected = "SHA256:R4kYrl6y+z+HnNG6/f7bYOrKrry51J9nXFV/iVAmTB0"  # Replace as needed

def get_sha256_fingerprint(key):
    """Generates the SHA256 fingerprint of an SSH key."""
    sha256_digest = base64.b64encode(hashlib.sha256(key.asbytes()).digest()).decode('utf-8')
    return f"SHA256:{sha256_digest}"

def retrieve_file():
    error_message = None  # To store any error message

    # Initialize SSH and SFTP clients
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # Ignore known_hosts policy
    
    try:
        # Attempt to establish SSH connection and verify fingerprint
        ssh.connect(hostname, username=username, password=password, banner_timeout=200)
        
        # Retrieve the host key
        server_key = ssh.get_transport().get_remote_server_key()
        fingerprint = server_key.fingerprint
        
        # Compare the actual fingerprint to the expected one
        if fingerprint != fingerprint_expected:
            raise ValueError("Server fingerprint does not match the expected value!")
        
        # If fingerprint matches, proceed with SFTP
        sftp = ssh.open_sftp()
        
        try:
            with sftp.file(file_path, "r") as remote_file:
                file_contents = remote_file.read().decode('utf-8')
                return {
                    'statusCode': 200,
                    'body': file_contents
                }
                
        except FileNotFoundError:
            error_message = "The specified file was not found on the server."
        except IOError as e:
            error_message = f"An error occurred while reading the file: {e}"
        finally:
            sftp.close()
    
    except paramiko.AuthenticationException:
        error_message = "Authentication failed. Please check your username or password."
    except paramiko.SSHException as e:
        error_message = f"SSH connection failed: {e}"
    except ValueError as e:
        error_message = str(e)  # For fingerprint mismatch
    finally:
        ssh.close()
    
    # Print error message if any error occurred
    if error_message:
        return {
            'statusCode': 404,
            'body': error_message
        }

def lambda_handler(event, context):
    results = retrieve_file()
    return results