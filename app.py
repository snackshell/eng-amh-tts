import tempfile
import edge_tts
import gradio as gr
import asyncio

language_dict = {
    "Amharic": {
        "Ameha": "am-ET-AmehaNeural",
        "Mekdes": "am-ET-MekdesNeural"
    }
}

async def text_to_speech_edge(text, speaker):
    voice = language_dict["Amharic"][speaker]
    
    try:
        communicate = edge_tts.Communicate(text, voice)
        
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_file:
            tmp_path = tmp_file.name
            await asyncio.wait_for(communicate.save(tmp_path), timeout=30)
            
        return tmp_path
        
    except asyncio.TimeoutError:
        error_msg = "ስህተት: ጊዜ አልቋል። እባክዎ እንደገና ይሞክሩ። (Timeout)"
        raise gr.Error(error_msg)
    except Exception as e:
        error_msg = f"ስህተት: ድምፅ መፍጠር አልተቻለም።\nError: {str(e)}"
        raise gr.Error(error_msg)

with gr.Blocks(title="Amharic TTS", theme=gr.themes.Soft()) as demo:
    gr.HTML("""
    <style>
        h1 { 
            color: #2E86C1; 
            text-align: center;
            background: linear-gradient(45deg, #FF007F, #2E86C1);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 30px;
            font-size: 2.5em;
        }
        .gradio-container {
            background: #f8f9fa !important;
        }
        .gradio-button { 
            background: linear-gradient(45deg, #FF007F, #2E86C1) !important; 
            color: white !important;
            border-radius: 8px !important;
            padding: 12px 24px !important;
        }
        .gradio-textbox, .gradio-dropdown { 
            border-color: #2E86C1 !important;
            border-radius: 8px !important;
            padding: 12px !important;
        }
        .gradio-label {
            color: #2E86C1 !important;
            font-weight: 600 !important;
        }
        .prose {
            max-width: 800px;
            margin: 0 auto;
        }
        .gradio-row {
            gap: 20px;
        }
    </style>
    <center>
        <h1>የአማርኛ ጽሑፍ ወደ ድምፅ ቀይር</h1>
    </center>
    """)

    with gr.Row():
        with gr.Column(scale=1):
            input_text = gr.Textbox(
                lines=5, 
                label="ጽሑፍ ያስገቡ",
                placeholder="ድምፅ ለመፍጠር ጽሑፍዎን ይጻፉ..."
            )
            speaker = gr.Dropdown(
                choices=["Ameha", "Mekdes"],
                value="Ameha",
                label="ድምፁን የሚያሰማ አርቲስት"
            )
            run_btn = gr.Button(
                value="ድምፅ ፍጠር", 
                variant="primary",
                scale=1
            )

        with gr.Column(scale=1):
            output_audio = gr.Audio(
                type="filepath",
                label="የተፈጠረ ድምፅ",
                elem_classes="output-audio"
            )

    run_btn.click(
        text_to_speech_edge,
        inputs=[input_text, speaker],
        outputs=output_audio
    )

if __name__ == "__main__":
    demo.launch(server_port=7860, share=False)
