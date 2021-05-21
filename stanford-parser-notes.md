# Stanford parser usage

## CLOB

+ Test:

        java -mx1g -cp "*" edu.stanford.nlp.parser.lexparser.LexicalizedParser -writeOutputFiles -outputFilesDirectory ~/Documents -sentences newline -tokenized -tagSeparator _ -tokenizerFactory edu.stanford.nlp.process.WhitespaceTokenizer -tokenizerMethod newCoreLabelTokenizerFactory edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz ~/Projects/corpora/CLOB-PTB-Tags/C-A01BA.txt

+ Full thing:

        java -mx2g -cp "*" edu.stanford.nlp.parser.lexparser.LexicalizedParser -writeOutputFiles -outputFilesDirectory ~/Projects/corpora/CLOB-PTB -sentences newline -tokenized -tagSeparator _ -tokenizerFactory edu.stanford.nlp.process.WhitespaceTokenizer -tokenizerMethod newCoreLabelTokenizerFactory edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz ~/Projects/corpora/CLOB-PTB-Tags/*.txt

+ Taps out at sent 8 of H01B.txt (340 characters)

+ Attempt 2 (In a new folder just in case):

        java -mx4g -cp "*" edu.stanford.nlp.parser.lexparser.LexicalizedParser -writeOutputFiles -outputFilesDirectory ~/Projects/corpora/CLOB-PTB2 -sentences newline -tokenized -tagSeparator _ -tokenizerFactory edu.stanford.nlp.process.WhitespaceTokenizer -tokenizerMethod newCoreLabelTokenizerFactory edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz ~/Projects/corpora/CLOB-PTB-Tags/C-[H-Z]*.txt

+ Ran out of memory again at C-H07B.txt. **Skipping the H's for now. Note that H01 is also busted now 02-06 are parsed okay.**

+ Attempt 3 (skips H):

        java -mx4g -cp "*" edu.stanford.nlp.parser.lexparser.LexicalizedParser -writeOutputFiles -outputFilesDirectory ~/Projects/corpora/CLOB-PTB2 -sentences newline -tokenized -tagSeparator _ -tokenizerFactory edu.stanford.nlp.process.WhitespaceTokenizer -tokenizerMethod newCoreLabelTokenizerFactory edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz ~/Projects/corpora/CLOB-PTB-Tags/C-[I-Z]*.txt

## FLOB

+ Attempt 1:

        java -mx4g -cp "*" edu.stanford.nlp.parser.lexparser.LexicalizedParser -writeOutputFiles -outputFilesDirectory ~/Projects/corpora/FLOB-PTB -sentences newline -tokenized -tagSeparator _ -tokenizerFactory edu.stanford.nlp.process.WhitespaceTokenizer -tokenizerMethod newCoreLabelTokenizerFactory edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz ~/Projects/corpora/FLOB-PTB-Tags/*.txt

+ It worked!

## LOB

        java -mx4g -cp "*" edu.stanford.nlp.parser.lexparser.LexicalizedParser -writeOutputFiles -outputFilesDirectory ~/Projects/corpora/LOB-PTB -sentences newline -tokenized -tagSeparator _ -tokenizerFactory edu.stanford.nlp.process.WhitespaceTokenizer -tokenizerMethod newCoreLabelTokenizerFactory edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz ~/Projects/corpora/LOB-PTB-Tags/*.TXT

Worked!

## Additional notes

+ Uploading to gdrive.

+ Need to do some QC

+ Still need to fix CLOB corpora.

