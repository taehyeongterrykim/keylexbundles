import glob
import re
import os
import math

def compute_keyness(target_path, reference_path, output_file="output.csv"):
    """
    Extract key lexical bundles between a target corpus and a reference corpus.

    target_path:    folder path or file path for a target corpus (e.g., 'user/data/target', 'data/target/*.txt', or 'data/target/a.txt')
    reference_path: folder path or file path for a reference corpus
    output_file:    CSV path to write results into (default: 'output.csv')
    """

    # Allow folder paths or explicit filenames.
    # In case of folder path, all *.txt in that directory are processed.
    def as_pattern(p):
        if p.endswith(".txt") or "*" in p or "?" in p or "[" in p:
            return p
        return os.path.join(p, "*.txt")

    path = as_pattern(target_path)
    path2 = as_pattern(reference_path)

    # Set up output file
    file_out = open(output_file, "w+", encoding="utf-8", errors="replace")

    # Initialize variables
    bundles = []
    text_counts = {}
    lexical_bundles = {}
    word_count = 0
    lexical_bundle_normed_frequencies = {}
    file_count = 0
    f_keyness = {}
    d_keyness = {}

    # Iterate over each file in the target corpus
    for file in glob.glob(path):
        print(file)
        line_count = 0
        text_bundles = []
        text_word_count = 0
        text_bundles_count = {}
        file_count += 1
        with open(file, encoding='utf-8', errors='ignore') as file_in:

            # Read the texts and preprocess each line
            text = list(file_in)
            for line in text:
                line_count += 1
                line = line.lower()
                line = re.sub('<p>|<h>', '', line)
                line = re.sub(r'\s-\s', ', ', line)
                line = re.sub(r'\s–\s', ', ', line)
                line = re.sub(r'-\s', ', ', line)
                line = re.sub(r'–\s', ', ', line)
                line = re.sub(r"[’‘'\"“”`´́]", '', line)

                # Split each line into sentences based on terminal punctuations
                if line_count > 0:
                    sentences = re.split(r'[.,?!;:]', line)

                    # Split each sentence into words
                    for sentence in sentences:
                        words = sentence.split()
                        length = len(words)

                        for i, word in enumerate(words):
                            # word = re.sub('[^\w|\s|\'|\-]', '', word)
                            word_count += 1
                            text_word_count += 1
                            if length - i >= 4:
                                current_bundles = " ".join(words[i:i + 4])
                                bundles.append(current_bundles)
                                text_bundles.append(current_bundles)

        # Remove repetitions to count for text dispersion
        unique_bundles = list(set(text_bundles))

        # Count the occurrences of each bundle in the current text
        for w in text_bundles:
            text_bundles_count[w] = text_bundles_count.get(w, 0) + 1

        # Normalize the occurrences to per 1000 words
        for key in text_bundles_count:
            text_bundles_count[key] = (text_bundles_count[key] / text_word_count) * 1000

        # Update global dictionary outside the loop
        for key in text_bundles_count:
            if key not in lexical_bundle_normed_frequencies:
                lexical_bundle_normed_frequencies[key] = []

            lexical_bundle_normed_frequencies[key].append(text_bundles_count[key])

        # Count the number of texts in which each bundle is used
        for w in unique_bundles:
            text_counts[w] = text_counts.get(w, 0) + 1

    # Count the raw total frequency of bundles
    for bundle in bundles:
        lexical_bundles[bundle] = lexical_bundles.get(bundle, 0) + 1

    mean_sd_dict = {}

    # Calculate mean and standard deviation of normalized frequencies
    for key, values in lexical_bundle_normed_frequencies.items():
        # Calculate mean value
        mean_value = sum(values) / file_count

        # Calculate population standard deviation
        NA = file_count - len(values)
        sum_squared_diff = sum((x - mean_value) ** 2 for x in values)

        # Adjust for missing values
        sum_squared_diff += (0 - mean_value) ** 2 * NA

        sd_value = (sum_squared_diff / file_count) ** 0.5

        mean_sd_dict[key] = {'mean': mean_value, 'sd': sd_value}

    # The same process is repeated for the reference corpus
    bundles2 = []
    text_counts2 = {}
    lexical_bundles2 = {}
    word_count2 = 0
    lexical_bundle_normed_frequencies2 = {}
    file_count2 = 0

    for file in glob.glob(path2):
        print(file)
        line_count2 = 0
        text_bundles2 = []
        text_word_count2 = 0
        text_bundles_count2 = {}
        file_count2 += 1
        with open(file, encoding='utf-8', errors='ignore') as file_in:
            text = list(file_in)
            for line in text:
                line_count2 += 1
                line = line.lower()
                line = re.sub('<p>|<h>', '', line)
                line = re.sub(r'\s-\s', ', ', line)
                line = re.sub(r'\s–\s', ', ', line)
                line = re.sub(r'-\s', ', ', line)
                line = re.sub(r'–\s', ', ', line)
                line = re.sub(r"[’‘'\"“”`´́]", '', line)

                if line_count2 > 0:
                    sentences = re.split(r'[.,?!;:]', line)

                    for sentence in sentences:
                        words = sentence.split()
                        length = len(words)

                        for i, word in enumerate(words):
                            # word = re.sub('[^\w|\s|\'|\-]', '', word)
                            word_count2 += 1
                            text_word_count2 += 1
                            if length - i >= 4:
                                current_bundles2 = " ".join(words[i:i + 4])
                                bundles2.append(current_bundles2)
                                text_bundles2.append(current_bundles2)

        unique_bundles2 = list(set(text_bundles2))

        for w in text_bundles2:
            text_bundles_count2[w] = text_bundles_count2.get(w, 0) + 1

        for key in text_bundles_count2:
            text_bundles_count2[key] = (text_bundles_count2[key] / text_word_count2) * 1000

        for key in text_bundles_count2:
            if key not in lexical_bundle_normed_frequencies2:
                lexical_bundle_normed_frequencies2[key] = []

            lexical_bundle_normed_frequencies2[key].append(text_bundles_count2[key])

        for w in unique_bundles2:
            text_counts2[w] = text_counts2.get(w, 0) + 1

    for bundle in bundles2:
        lexical_bundles2[bundle] = lexical_bundles2.get(bundle, 0) + 1

    mean_sd_dict2 = {}

    for key, values in lexical_bundle_normed_frequencies2.items():
        mean_value = sum(values) / file_count2

        NA = file_count2 - len(values)
        sum_squared_diff = sum((x - mean_value) ** 2 for x in values)

        sum_squared_diff += (0 - mean_value) ** 2 * NA

        sd_value = (sum_squared_diff / file_count2) ** 0.5

        mean_sd_dict2[key] = {'mean': mean_value, 'sd': sd_value}

    # Calculate log-likelihood formula for each word in target dictionary
    for i in (lexical_bundles):

        freq_T = lexical_bundles[i]
        freq_R = 0

        # If the current word is in the reference corpus then use this formula
        if i in lexical_bundles2:
            freq_R = lexical_bundles2[i]
            E_T = word_count * ((freq_T + freq_R) / (word_count + word_count2))
            E_R = word_count2 * ((freq_T + freq_R) / (word_count + word_count2))
            G2 = 2 * ((freq_T * math.log(freq_T / E_T)) + (freq_R * math.log(freq_R / E_R)))
            if (freq_R / E_R) > (freq_T / E_T):
                G2 = (G2 * -1)
            f_keyness[i] = G2

        # If the current word is not in the reference corpus use this formula
        else:
            E_T = word_count * (freq_T + freq_R) / (word_count + word_count2)
            E_R = word_count2 * (freq_T + freq_R) / (word_count + word_count2)
            G2 = 2 * (freq_T * math.log(freq_T / E_T))
            f_keyness[i] = G2

    # Calculate log-likelihood formula for each word in target dictionary
    for i in (text_counts):

        freq_T = text_counts[i]
        freq_R = 0

        # If the current word is in the reference corpus then use this formula
        if i in text_counts2:
            freq_R = text_counts2[i]
            E_T = file_count * ((freq_T + freq_R) / (file_count + file_count2))
            E_R = file_count2 * ((freq_T + freq_R) / (file_count + file_count2))
            G2 = 2 * ((freq_T * math.log(freq_T / E_T)) + (freq_R * math.log(freq_R / E_R)))
            if (freq_R / E_R) > (freq_T / E_T):
                G2 = (G2 * -1)
            d_keyness[i] = G2

        # If the current word is not in the reference corpus use this formula
        else:
            E_T = file_count * (freq_T + freq_R) / (file_count + file_count2)
            E_R = file_count2 * (freq_T + freq_R) / (file_count + file_count2)
            G2 = 2 * (freq_T * math.log(freq_T / E_T))
            d_keyness[i] = G2

    file_out.write(
        "lexical bundle, whole-corpus frequency keyness, text dispersion keyness, mean text frequency keyness, raw frequency (target), normed frequency (target), text dispersion (target), mean of normed frequency (target), sd of normed frequency (target), raw frequency (reference), normed frequency (reference), text dispersion (reference), mean of normed frequency (reference), sd of normed frequency (reference) \n")

    for i in sorted(d_keyness, key=lambda x: (d_keyness[x], lexical_bundles.get(x,0)), reverse=True):
        if i in lexical_bundles2 and i in text_counts2 and lexical_bundles[i] >= 1 and text_counts[i] >= 1:
            # Write lexical bundle information to the output file for a bundle that satisfies the threshold
            mean1 = mean_sd_dict[i]['mean']
            mean2 = mean_sd_dict2[i]['mean']
            sd1 = mean_sd_dict[i]['sd']
            sd2 = mean_sd_dict2[i]['sd']

            # Compute mean text frequency keyness
            denominator = math.sqrt((sd1 ** 2 + sd2 ** 2) / 2)
            mean_keyness = (mean1 - mean2) / denominator if denominator != 0 else 0

            file_out.write(
                str(i) + "," + str(f_keyness[i]) + "," + str(d_keyness[i]) + "," + str(mean_keyness) + "," +  str(lexical_bundles[i]) + "," +
                str(lexical_bundles[i] / word_count * 1000) + "," + str(text_counts[i]) + "," + str(mean1) + "," + str(sd1) + "," +
                str(lexical_bundles2[i]) + "," + str(lexical_bundles2[i] / word_count2 * 1000) + "," + str(text_counts2[i]) + "," + str(mean2) + "," + str(sd2) + "," + "\n")

        elif i not in lexical_bundles2 and lexical_bundles[i] >= 1 and text_counts[i] >= 1:
            mean1 = mean_sd_dict[i]['mean']
            sd1 = mean_sd_dict[i]['sd']
            mean2 = 0.0
            sd2   = 0.0

            denominator = math.sqrt((sd1 ** 2 + sd2 ** 2) / 2)
            mean_keyness = (mean1 - mean2) / denominator if denominator != 0 else 0

            file_out.write(
                str(i) + "," + str(f_keyness[i]) + "," + str(d_keyness[i]) + "," + str(mean_keyness) + "," + str(lexical_bundles[i]) + "," +
                str(lexical_bundles[i] / word_count * 1000) + "," + str(text_counts[i]) + "," + str(mean1) + "," + str(sd1) +
                ",0,0,0,0,0\n")

    print(f"Keyness result is saved to {output_file}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Extract key lexical bundles between two corpora.")
    parser.add_argument("target", help="Path to folder with target corpus .txt files")
    parser.add_argument("reference", help="Path to folder with reference corpus .txt files")
    parser.add_argument("-o", "--output", default="output.csv", help="Output CSV filename (default: output.csv)")

    args = parser.parse_args()
    compute_keyness(args.target, args.reference, args.output)
