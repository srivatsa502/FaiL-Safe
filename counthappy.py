import json
import random


input_file = "C:/Users/Sri Vatsa/Desktop/FaiL-Safe Benchmark/ToolBench/data/Newdata.jsonl"
output_file = "C:/Users/Sri Vatsa/Desktop/FaiL-Safe Benchmark/ToolBench/data/PaladinEvalData_modified.jsonl"

cnt=0
error=""
error_codes = [
    "400", "401", "403", "404", "500", "503", "408",  # Request Timeout = 408
    "429", "409", "410", "411", "412", "413", "414", "415", "416", "417", "418",
    "421", "422", "423", "424", "425", "426", "428", "431",
    "444", "451", "498", "499",
    "501", "502", "504", "505", "507", "508", "510", "511",
    "529", "530", "540", "598", "599"
]
injected=False

# Trajectories= {
#     "400" : {
#         "Assistant (the Api)" :"Thought:I ecncoutnered a 404 error so I should re examine data  \n (new line) Action: re examine call,check parameter formatting, and re-issue the call with corrected parameters.",
#         "Function" : "Okay I found the mistake",
#         "Assitant": "Thoughts: Now that I found the mistake I should reformat \n Action: Reformatting everything \n Action input {reformatted call here}",
#         "Function":"Call succes"
#     },
#     "405" : {
#         "Assistant (the Api)" :"HMMM i gotta do Wahetevr the hell the first step is",
#         "Function" : "Okay so this shit happened after the first step",
#         "Assitant": "Okay now that this happened I gotta do this",
#         "Function":"HORRAYYY YOU DID ITTT"
#     },
# }


with open(input_file, "r", encoding="utf-8") as infile, open(output_file, "w", encoding="utf-8") as outfile:
    for line in infile:
        obj = json.loads(line)
        convos = obj.get("conversations", [])
        for idx,message in enumerate(convos):
            value = message.get("value", "")
            for code in error_codes:
                if code in value:
                    # Truncate and inject recovery actions with 50% chance
                    if random.random() < 0.5 and code in error_codes:
                        new_convos = convos[:idx + 1]  # keep up to and including the error
                          # inject recovery
                        injected = True
                    break
            if injected:
                break
        if not injected:
            new_convos = convos  # leave unchanged

        obj["conversations"] = new_convos
        outfile.write(json.dumps(obj, ensure_ascii=False) + "\n")

