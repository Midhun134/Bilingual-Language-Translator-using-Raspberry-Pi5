# import codecs

# def combine_files(text_file, ocaml_file, output_file):
#     try:
#         with codecs.open(text_file, 'r', encoding='utf-8') as tf, \
#              codecs.open(ocaml_file, 'r', encoding='utf-8') as of, \
#              codecs.open(output_file, 'w', encoding='utf-8') as outf:
#             # Read lines from both files
#             text_lines = tf.readlines()
#             ocaml_lines = of.readlines()
            
#             # Ensure both files have the same number of lines
#             if len(text_lines) != len(ocaml_lines):
#                 raise ValueError("Files have different number of lines.")
            
#             # Combine lines from both files
#             #for text_line, ocaml_line in zip(text_lines, ocaml_lines):
#              #   outf.write(f"{text_line.strip()} | {ocaml_line.strip()}\n")
                
#     except Exception as e:
#         print(f"Error: {e}")

# # File paths
# train_src = 'train.en'
# train_tgt = 'train.ml'
# val_src = 'valid.en'
# val_tgt = 'valid.ml'
# test_src = 'test.en'
# test_tgt = 'test.ml'

# combine_files(train_src, train_tgt, 'C:/Users/midhu/Downloads/en-ml.txt/train.txt')
# combine_files(val_src, val_tgt, 'C:/Users/midhu/Downloads/en-ml.txt/valid.txt')
# combine_files(test_src, test_tgt, 'C:/Users/midhu/Downloads/en-ml.txt/test.txt')


# import codecs

# def combine_files(input_files, output_file):
#     with codecs.open(output_file, 'w', encoding='utf-8') as outf:
#         for file_path in input_files:
#             with codecs.open(file_path, 'r', encoding='utf-8') as infile:
#                 outf.write(infile.read())
#                 outf.write('\n')  # Optional: add a newline between files

# # File paths
# train_src = ['train.en', 'train.ml']
# val_src = ['valid.en', 'valid.ml']
# test_src = ['test.en', 'test.ml']

# # Output file paths
# train_output = 'C:/Users/midhu/Downloads/en-ml.txt/train.txt'
# val_output = 'C:/Users/midhu/Downloads/en-ml.txt/valid.txt'
# test_output = 'C:/Users/midhu/Downloads/en-ml.txt/test.txt'

# # Combine files
# combine_files(train_src, train_output)
# combine_files(val_src, val_output)
# combine_files(test_src, test_output)



#to check if a file is utf-8 encoded or not
# def is_utf8(filename):
#     try:
#         with open(filename, 'r', encoding='utf-8') as f:
#             f.read()
#         return True
#     except UnicodeDecodeError:
#         return False

# filename = 'data-bin/train.en'
# if is_utf8(filename):
#     print(f"{filename} is UTF-8 encoded.")
# else:
#     print(f"{filename} is not UTF-8 encoded.")