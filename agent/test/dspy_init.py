import os
import dspy
from dotenv import load_dotenv

load_dotenv()
model_server = os.environ.get("LLM_OPENAI_API")
model_name = os.environ.get("LLM_MODEL_NAME")
api_key = os.environ.get("LLM_OPENAI_API_KEY")

lm = dspy.OpenAI(model=model_name, api_base=f"{model_server}/", api_key=api_key, max_tokens=24000)
colbertv2_wiki17_abstracts = dspy.ColBERTv2(url='http://20.102.90.50:2017/wiki17_abstracts')
dspy.settings.configure(lm=lm,rm=colbertv2_wiki17_abstracts)

from dsp.utils import deduplicate


class RAGSignature(dspy.Signature):
    """根据给定的上下文回答问题。"""

    context = dspy.InputField(desc="可能包含相关事实")
    question = dspy.InputField()
    answer = dspy.OutputField(desc="不超过 1 段的答案")


class GenerateSearchQuery(dspy.Signature):
    """编写一个简单的搜索查询，以帮助回答复杂的问题。"""
    context = dspy.InputField(desc="可能包含相关事实")
    question = dspy.InputField()
    query = dspy.OutputField()


class MultiHopChainOfThoughtRAG(dspy.Module):
    def __init__(self, passages_per_hop=3, max_hops=2):
        super().__init__()

        self.generate_query = [dspy.ChainOfThought(GenerateSearchQuery) for _ in range(max_hops)]
        self.retrieve = dspy.Retrieve(k=passages_per_hop)
        self.generate_answer = dspy.ChainOfThought(RAGSignature)
        self.max_hops = max_hops
        self.k = passages_per_hop

    def forward(self, question):
        context = []

        for hop in range(self.max_hops):
            query = self.generate_query[hop](context=context, question=question).query
            passages = self.retrieve(query, k=self.k)
            print(passages)
            context = deduplicate(context + passages)
        pred = self.generate_answer(context=context, question=question)
        return dspy.Prediction(context=context, answer=pred.answer)

multi_hop_rag = MultiHopChainOfThoughtRAG()
query = "过量服用扑热息痛会导致肾衰竭吗？如果我一次服用 3 克，算过量吗？"
response = multi_hop_rag(query).answer
print(response)
