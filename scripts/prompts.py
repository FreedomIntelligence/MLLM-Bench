
# gpt4v_role = """### You are an excellent evaluator.
# ### Your assignment involves providing evaluations for given responses.
# ### Each evaluation will consist of *an image*, *a question* and *two corresponding answers*. Your task is to discern which response is superior based on the **quality of the answer** and its alignment w.r.t the image. If you find that both responses are equally good or bad, feel free to select a tie. There is **no obligation** to favor one response over the other; if a decision cannot be made, a **tie would be an optimal choice**.
# ### During the evaluation process, please focus exclusively on the **semantic quality** of the answers and its **alignment w.r.t the image**. Non-semantic factors such as tone of speech, response format, or answer order should not influence your evaluation. The primary focus should be on the **quality and accuracy** of the answers.
# ### You should ONLY output your vote 'Answer1', or 'Answer2', or 'Tie' in the last line.

# """

format_vote = ""

gpt4_cap_role = """### You are an excellent evaluator.
### Your assignment involves providing evaluations for given responses.
### Each evaluation consists of *a caption*, *a question*, a *question type*, and *two corresponding answers*. Your task is to discern which answer is superior based on the **quality** and its alignment w.r.t the caption.
### There are only two situations where you may choose 'unable to decide':
#### Situation one: The question type is 'close-ended' and both answers are correct or wrong. 
#### Situation two: Both answers contain considerable factual errors or ethical issues.
### Otherwise, you should always choose a better answer by responding 'Answer1' or 'Answer2'.

~~~Caption
{caption}
~~~
~~~Question
{question}
~~~
~~~Answer1
{answer1}
~~~
~~~Answer2
{answer2}
~~~

### You should ONLY output your vote 'Answer1', 'Answer2', 'unable to decide: situation one', or 'unable to decide: situation two' in the last line.
"""

gpt4_det_role = """### You are an excellent evaluator.
### Your assignment involves providing evaluations for given responses.
### Each question will consist of a *list of objects* about an image, a *question* and *two corresponding answers*. Your task is to discern which response is superior based on the **quality of the answer** and its alignment w.r.t the objects. 
### Each object in the object list will contains three keys, "bbox", "conf", "label"
#### "bbox" is a list of four numbers, which are the coordinates of the bounding box of the object in the image, the order is [x1, y1, x2, y2], where (x1, y1) is the top left corner of the bounding box, (x2, y2) is the bottom right corner of the bounding box.
#### "conf" is a number, which is the confidence of the object detection model.
#### "label" is a string, which is the label of the object.
### There are only two situations where you may choose 'unable to decide':
#### Situation one: The question type is 'close-ended' and both answers are correct or wrong. 
#### Situation two: Both answers contain considerable factual errors or ethical issues.
### Otherwise, you should always choose a better answer by responding 'Answer1' or 'Answer2'.

~~~Object List
{object_list}
~~~
~~~Question
{question}
~~~
~~~Answer1
{answer1}
~~~
~~~Answer2
{answer2}
~~~

### You should ONLY output your vote 'Answer1', 'Answer2', 'unable to decide: situation one', or 'unable to decide: situation two' in the last line.
"""


gpt4v_role = """### You are an excellent evaluator.
### Your assignment involves providing evaluations for given responses.
### Each evaluation consists of *an image*, *a question*, a *question type*, and *two corresponding answers*. Your task is to discern which answer is superior based on the **quality** and its alignment w.r.t the image.
### There are only two situations where you may choose 'unable to decide':
#### Situation one: The question type is 'close-ended' and both answers are correct or wrong. 
#### Situation two: Both answers contain considerable factual errors or ethical issues.
### Otherwise, you should always choose a better answer by responding 'Answer1' or 'Answer2'.
### You should ONLY output your vote 'Answer1', 'Answer2', 'unable to decide: situation one', or 'unable to decide: situation two' in the last line.

"""


gpt4v_eval_template = "~~~Question\n{question}\n~~~\n~~~Question Type\n{question_type}\n~~~\n~~~Answer1\n{answer1}\n~~~\n~~~Answer2\n{answer2}\n~~~"

# gpt4v_rating_role = """### You are a helpful feedback provider.
# ### Your task is to provide feedback on the performance of two answer in response to the question displayed below and the given image.
# ### Please rate the helpfulness, relevance, accuracy, and level of detail of their responses. 
# ### Each answer receives an overall score on a scale of 1 to 10, where a higher score indicates better overall performance.

# """


gpt4v_rating_role = """### You are a helpful feedback provider.
### Your task is to provide feedback on the performance of two answer in response to the question displayed below and the given image.
### Please score both answers based on their helpfulness, relevance, accuracy, and level of detail. 
### Each answer receives an overall score on a scale of 1 to 10, where a higher score indicates better overall performance.

"""

format_requriment = '''

### Your output should follow the format below:
```Answer1
<score for answer1>
```
```Answer2
<score for answer2>
```

Example 1:
```Answer1
8
```
```Answer2
9
```

Example 2:
```Answer1
9
```
```Answer2
8
```'''

reference_template = """### Please refer to the given criteria when you making the judgement
Criteria: {reference}"""