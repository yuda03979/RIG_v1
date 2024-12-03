# getting started

### roadmap:
- the package is in EltaProject folder.
- the benchmark folder its for the data, evaluation, and maybe more.


# Installation

### - steps:
1. place the data_directory in your desire place.
2. RECOMMENDED: in EltaProject/globals.py, set the data_directory and the db_file_name. the data_directory should be "/bla/bla/", and the db_file_name should be "blabla.csv".
3. with your terminal, go to EltaProject folder and run:
   pip
    ```sh
   pip install -e .
   ```

### - notes:
* make sure you've installed the requirements.txt
* make sure you use the same interpreter, you enter the paths in the correct way.
* dont run those commands from jupiter notebook. can cause some problems.
* to uninstall run: `pip uninstall RIG` 
* let's go!

## how to use:


```python
from RIG import RuleInstanceGenerator
```


```python
# all the parameters are optional, except the data_directory, unless you change it in the globals. it is also recommended to change db_file_name

rig = RuleInstanceGenerator(
    data_directory="/Users/yuda/PycharmProjects/EltaBenchmark/data_directory/",  # data_directory="/.../" 
    db_file_name="db_data.csv"  # db_file_name="blabla.csv"
)
```

here you will see some lines. 
its OK, dont worry.


 llama_new_context_with_model: n_ctx_per_seq (1024) < n_ctx_train (8192) -- the full capacity of the model will not be utilized
 ggml_metal_init: skipping kernel_get_rows_bf16                     (not supported)
 ggml_metal_init: skipping kernel_mul_mv_bf16_f32                   (not supported)
 ggml_metal_init: skipping kernel_mul_mv_bf16_f32_1row              (not supported)
 ggml_metal_init: skipping kernel_mul_mv_bf16_f32_l4                (not supported)
 ggml_metal_init: skipping kernel_mul_mv_bf16_bf16                  (not supported)
 ggml_metal_init: skipping kernel_mul_mv_id_bf16_f32                (not supported)
 ggml_metal_init: skipping kernel_mul_mm_bf16_f32                   (not supported)
 ggml_metal_init: skipping kernel_mul_mm_id_bf16_f32                (not supported)
 ggml_metal_init: skipping kernel_flash_attn_ext_bf16_h64           (not supported)
 ggml_metal_init: skipping kernel_flash_attn_ext_bf16_h80           (not supported)
 ggml_metal_init: skipping kernel_flash_attn_ext_bf16_h96           (not supported)
 ggml_metal_init: skipping kernel_flash_attn_ext_bf16_h112          (not supported)
 ggml_metal_init: skipping kernel_flash_attn_ext_bf16_h128          (not supported)
 ggml_metal_init: skipping kernel_flash_attn_ext_bf16_h256          (not supported)
 ggml_metal_init: skipping kernel_flash_attn_ext_vec_bf16_h128      (not supported)
 ggml_metal_init: skipping kernel_flash_attn_ext_vec_bf16_h256      (not supported)
 ggml_metal_init: skipping kernel_cpy_f32_bf16                      (not supported)
 ggml_metal_init: skipping kernel_cpy_bf16_f32                      (not supported)
 ggml_metal_init: skipping kernel_cpy_bf16_bf16                     (not supported)


```python


# if you want to adjust the parameters
rig2 = RuleInstanceGenerator(
    data_directory="/Users/yuda/PycharmProjects/EltaBenchmark/data_directory/",
    db_file_name="db_data.csv",
    rag_threshold=0.5,
    max_context_length=1024,
    max_new_tokens=512,
    n_threads=5
)
```
 llama_new_context_with_model: n_ctx_per_seq (1024) < n_ctx_train (8192) -- the full capacity of the model will not be utilized
 ggml_metal_init: skipping kernel_get_rows_bf16                     (not supported)
 ggml_metal_init: skipping kernel_mul_mv_bf16_f32                   (not supported)
 ggml_metal_init: skipping kernel_mul_mv_bf16_f32_1row              (not supported)
 ggml_metal_init: skipping kernel_mul_mv_bf16_f32_l4                (not supported)
 ggml_metal_init: skipping kernel_mul_mv_bf16_bf16                  (not supported)
 ggml_metal_init: skipping kernel_mul_mv_id_bf16_f32                (not supported)
 ggml_metal_init: skipping kernel_mul_mm_bf16_f32                   (not supported)
 ggml_metal_init: skipping kernel_mul_mm_id_bf16_f32                (not supported)
 ggml_metal_init: skipping kernel_flash_attn_ext_bf16_h64           (not supported)
 ggml_metal_init: skipping kernel_flash_attn_ext_bf16_h80           (not supported)
 ggml_metal_init: skipping kernel_flash_attn_ext_bf16_h96           (not supported)
 ggml_metal_init: skipping kernel_flash_attn_ext_bf16_h112          (not supported)
 ggml_metal_init: skipping kernel_flash_attn_ext_bf16_h128          (not supported)
 ggml_metal_init: skipping kernel_flash_attn_ext_bf16_h256          (not supported)
 ggml_metal_init: skipping kernel_flash_attn_ext_vec_bf16_h128      (not supported)
 ggml_metal_init: skipping kernel_flash_attn_ext_vec_bf16_h256      (not supported)
 ggml_metal_init: skipping kernel_cpy_f32_bf16                      (not supported)
 ggml_metal_init: skipping kernel_cpy_bf16_f32                      (not supported)
 ggml_metal_init: skipping kernel_cpy_bf16_bf16                     (not supported)


## adding new rule type


```python


# return True or False
succeed = rig.new_rule_type('system_failure_file.json')  # loading from file

if succeed:
    print("rule type added successfully")
else:
    print("error! failed to add the rule_type")
```

rule type added successfully



```python
import json
with open('system_failure_file.json', 'r') as file:
    rule_type_dict = json.load(file)

succeed = rig.new_rule_type(rule_type_dict)  # loading from dict


if succeed:
    print("rule type added successfully")
else:
    print("error! failed to add the rule_type")
```
rule type added successfully



```python
# get list of existing rule types:
rig.get_rule_types()
```
 ['missile malfunction',
  'tactical error',
  'missile failure',
  'launch failure',
  'platoon report',
  'moral failure',
  'encryption flaw',
  'espionage suspect',
  'corruption scandal',
  'betrayal risk',
  'leadership breakdown',
  'radar error monitoring',
  'personnel sabotage',
  'satellite disruption',
  'bomb failure',
  'defection threat',
  'attack overview',
  'fire control',
  'disloyal soldier',
  'equipment malfunction',
  'command incompetence',
  'supply shortage',
  'system failure',
  'covert agent',
  'suspected person']



## get rule instance from free text


```python
free_text = "Alright, let's dive in. We're looking at 'Exploitation Scenario 789'. The crux of the matter is, there's this individual, going by the ID 'XYZ789', who's been involved in an exploitation failure. The level of seriousness? I'd estimate about three. The breach? Fairness. Not good, not good at all. When did we spot this? Well, the detection time isn't clear. And the context? Personal. Yes, it's a pretty serious situation"

response = rig.get_rule_instance(free_text) # return dictionary
```


```python
response.keys()
```

dict_keys(['rule_instance', 'error', 'error_message', 'free_text', 'type_name', 'rag_score', 'model_response', 'schema', 'time', 'inference_time'])




```python
response["rule_instance"] # the package response
```


output:

    {'_id': '00000000-0000-0000-0000-000000000000',
     'description': 'string',
     'isActive': True,
     'lastUpdateTime': '00/00/0000 00:00:00',
     'params': {'individualID': 'XYZ789',
      'failureType': 'Fairness',
      'detectionTime': 'null',
      'ethicalViolation': 'null',
      'context': 'Personal'},
     'ruleInstanceName': 'Exploitation Scenario 789',
     'severity': 3,
     'ruleType': 'structured',
     'ruleOwner': '',
     'ruleTypeId': '7a2f6c94-2b4f-4d9d-8a77-d11f7c7cc8fc',
     'eventDetails': [{'objectName': 'Moral',
       'objectDescription': None,
       'timeWindowInMilliseconds': 0,
       'useLatest': False}],
     'additionalInformation': {},
     'presetId': '00000000-0000-0000-0000-000000000000'}




```python
# giving us feedback on the response. it will help us to improve the project. it stores in .logs file, without internet connection.
rig.feedback(True)  # or 0.8, or what ever you can  
```
thank you :)



## using the GUI
very basic, work only with the globals file constant


```python
from RIG.src.Utils.GUI import run_gui
run_gui()
```

llama_new_context_with_model: n_ctx_per_seq (1024) < n_ctx_train (8192) -- the full capacity of the model will not be utilized
ggml_metal_init: skipping kernel_get_rows_bf16                     (not supported)
ggml_metal_init: skipping kernel_mul_mv_bf16_f32                   (not supported)
ggml_metal_init: skipping kernel_mul_mv_bf16_f32_1row              (not supported)
ggml_metal_init: skipping kernel_mul_mv_bf16_f32_l4                (not supported)
ggml_metal_init: skipping kernel_mul_mv_bf16_bf16                  (not supported)
ggml_metal_init: skipping kernel_mul_mv_id_bf16_f32                (not supported)
ggml_metal_init: skipping kernel_mul_mm_bf16_f32                   (not supported)
ggml_metal_init: skipping kernel_mul_mm_id_bf16_f32                (not supported)
ggml_metal_init: skipping kernel_flash_attn_ext_bf16_h64           (not supported)
ggml_metal_init: skipping kernel_flash_attn_ext_bf16_h80           (not supported)
ggml_metal_init: skipping kernel_flash_attn_ext_bf16_h96           (not supported)
ggml_metal_init: skipping kernel_flash_attn_ext_bf16_h112          (not supported)
ggml_metal_init: skipping kernel_flash_attn_ext_bf16_h128          (not supported)
ggml_metal_init: skipping kernel_flash_attn_ext_bf16_h256          (not supported)
ggml_metal_init: skipping kernel_flash_attn_ext_vec_bf16_h128      (not supported)
ggml_metal_init: skipping kernel_flash_attn_ext_vec_bf16_h256      (not supported)
ggml_metal_init: skipping kernel_cpy_f32_bf16                      (not supported)
ggml_metal_init: skipping kernel_cpy_bf16_f32                      (not supported)
ggml_metal_init: skipping kernel_cpy_bf16_bf16                     (not supported)


* Running on local URL:  http://0.0.0.0:8000

To create a public link, set `share=True` in `launch()`.

<img src="gui.png" alt="GUI" width="10000" />