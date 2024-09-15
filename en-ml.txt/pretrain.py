import random
#this is done to make the dataset format into farseq which is binary because helsinky is trained on farseq format
def read_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        return file.readlines()

def write_file(filepath, lines):
    with open(filepath, 'w', encoding='utf-8') as file:
        for line in lines:
            file.write(line)

def split_dataset(en_lines, ml_lines, train_ratio=0.8, valid_ratio=0.1, test_ratio=0.1):
    assert len(en_lines) == len(ml_lines), "The number of lines in the two files should be the same"
    
    data = list(zip(en_lines, ml_lines))
    random.shuffle(data)
    
    train_size = int(train_ratio * len(data))
    valid_size = int(valid_ratio * len(data))
    
    train_data = data[:train_size]
    valid_data = data[train_size:train_size + valid_size]
    test_data = data[train_size + valid_size:]
    
    return train_data, valid_data, test_data

# File paths
english_file = 'ELRC_2922.en-ml.en'
malayalam_file = 'ELRC_2922.en-ml.ml'

# Read the files
en_lines = read_file(english_file)
ml_lines = read_file(malayalam_file)

# Split the dataset
train_data, valid_data, test_data = split_dataset(en_lines, ml_lines)

# Write the splits to files
write_file('train.en', [line[0] for line in train_data])
write_file('train.ml', [line[1] for line in train_data])
write_file('valid.en', [line[0] for line in valid_data])
write_file('valid.ml', [line[1] for line in valid_data])
write_file('test.en', [line[0] for line in test_data])
write_file('test.ml', [line[1] for line in test_data])

print("Dataset successfully split into train, validation, and test sets.")

#fairseq-preprocess --source-lang en --target-lang ml --trainpref C:\Users\midhu\Downloads\en-ml.txt\train --validpref C:\Users\midhu\Downloads\en-ml.txt\valid --testpref C:\Users\midhu\Downloads\en-ml.txt\test --destdir C:\Users\midhu\Downloads\en-ml.txt\data-bin --workers 4
#run on command prompt since in command prompt u cannot run with / after each command