FROM goharbor.ebsig.com/library/python:3.10.13-ai-lib
ARG build
ARG commit
LABEL ai.mindforce.build=$build
LABEL ai.mindforce.commit=$commit
WORKDIR /usr/local/mindforce-ai-assistant
COPY . /usr/local/mindforce-ai-assistant
RUN pip config --user set global.progress_bar off && pip install -r requirements.txt -i https://pypi.mirrors.ustc.edu.cn/simple/
CMD ["python","main.py"]