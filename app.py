import streamlit as st
from chatbot import ask_perplexity

st.set_page_config(page_title="冰箱食材推薦系統", layout="wide")
st.title("🥬 冰箱食材 X 食譜推薦")

with st.sidebar:
    st.header("🔧 設定")
    api_key = st.text_input("請輸入 Perplexity API Key", type="password")
    ingredients = st.text_input("請輸入冰箱食材（用逗號分隔）", "雞肉, 馬鈴薯, 絲瓜, 蛤蜊")

if api_key:
    st.subheader("🍽️ AI 食譜推薦")
    if st.button("推薦食譜"):
        prompt = f"""我冰箱裡有：{ingredients}。
請推薦我 5 道可以做的家常料理。每道料理請賦予有創意、有畫面感、有特色的名字（可加入形容詞、氣氛、料理方式）。請依下列格式清楚分段回覆：

🥘 食譜(加上數字1-5)
🍽️ 料理名稱：（請創意命名，如「黃金絲瓜瀑布蛋」、「香濃白湯炆絲瓜」）
🧂 所需食材：
🧑‍🍳 烹調流程：（請用 3~5 步驟分段說明）"""
        with st.spinner("AI 正在構思創意料理中..."):
            recipes = ask_perplexity(api_key, prompt)
            st.session_state["last_recipes"] = recipes

    if "last_recipes" in st.session_state:
        st.markdown(st.session_state["last_recipes"])

    st.subheader("🧠 與料理助理聊聊")
    question = st.text_input("你對上面的創意食譜有什麼問題？")
    if question:
        if "last_recipes" in st.session_state:
            combined_prompt = f"""以下是我剛剛獲得的食譜建議：\n{st.session_state['last_recipes']}\n\n現在我有個問題：{question}"""
        else:
            combined_prompt = question
        with st.spinner("AI 助理回覆中..."):
            reply = ask_perplexity(api_key, combined_prompt)
            st.markdown(reply)
else:
    st.warning("請在左側輸入 Perplexity API Key 才能使用功能")
