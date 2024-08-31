def is_pdf(file_path):
    try:
        with open(file_path, 'rb') as file:
            header = file.read(5)  # 读取文件的前5个字节
            return header == b'%PDF-'
    except Exception as e:
        print(f"Error occurred: {e}")
        return False
    
def is_pdf_b(binary_content):
    return binary_content[:5] == b'%PDF-'


if __name__ == '__main__':

    # 示例使用
    file_path = 'example.pdf'
    if is_pdf(file_path):   
        print(f"{file_path} is a PDF file.")
    else:
        print(f"{file_path} is not a PDF file.")