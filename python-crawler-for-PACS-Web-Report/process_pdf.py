
import random
import io
import re
import os
import pdfminer.settings
pdfminer.settings.STRICT = False
import pdfminer.high_level
import pdfminer.layout


from using_logger import *

def extract_raw_text(pdf_filename):
    output = io.StringIO()
    laparams = pdfminer.layout.LAParams() # Using the defaults seems to work fine

    with open(pdf_filename, "rb") as pdffile:
        pdfminer.high_level.extract_text_to_fp(pdffile, output, laparams=laparams)

    return output.getvalue()



def process_pdf(exam,localpath,get_count=0,pass_count=0,pdf_error=0):
    results = extract_raw_text(localpath)
    # if results.find('前列腺') != -1:
    # if re.search('前列腺|睾丸',results): # is not None
    if re.search('子宫|卵巢',results): # is not None
        # print('{0} get'.format(exam))
        logger.error('{0} get'.format(exam))
        try:
            os.rename(localpath,localpath[0:-4]+'_{0}_marked.pdf'.format(exam))
        except:
            try:
                os.rename(localpath, localpath[0:-4] + '_{0}_marked.pdf'.format(random.sample('adcdefgh', 5)))
            except Exception as renameerror:
                logger.error(renameerror)

        get_count +=1
    elif results.find('诊断') != -1:
        # print('exam pass')
        logger.info('{0} pass'.format(exam))
        os.remove(localpath)
        pass_count +=1
    else:
        logger.error('{0} pdf parse failed'.format(exam))
        pdf_error += 1
        try:
            os.rename(localpath,localpath[0:-4]+'_{0}_parsefailed.pdf'.format(exam))
        except:
            try:
                os.rename(localpath, localpath[0:-4] + '_parsefailed_{0}.pdf'.format(random.sample('adcdefgh', 5)))
            except Exception as renameerror:
                logger.error(renameerror)

    return get_count,pass_count,pdf_error

if __name__ == '__main__':
    # localpath = "PDF\\1468413.pdf"
    # exam = '10640811'
    results = '前列腺'
    if re.search('前列腺|睾丸',results):
        print(1)
    print(re.search('前列腺|睾丸',results))
    # # process_pdf(exam,localpath)
    # print(parse(localpath))

    # print(extract_raw_text('PDF\\1468413.pdf'))
