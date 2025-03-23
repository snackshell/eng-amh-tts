import tempfile
import edge_tts
import gradio as gr
import asyncio

language_dict = {
    "Amharic": {
        "Ameha": "am-ET-AmehaNeural",
        "Mekdes": "am-ET-MekdesNeural"
    },
    "English": {
        "Ryan": "en-GB-RyanNeural",
        "Clara": "en-CA-ClaraNeural"
    }
}

async def text_to_speech_edge(text, language, speaker):
    voice = language_dict[language][speaker]
    
    try:
        communicate = edge_tts.Communicate(text, voice)
        
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_file:
            tmp_path = tmp_file.name
            await asyncio.wait_for(communicate.save(tmp_path), timeout=30)
            
        return tmp_path
        
    except asyncio.TimeoutError:
        error_msg = "ስህተት: ጊዜ አልቋል። እባክዎ እንደገና ይሞክሩ። (Timeout)" if language == "Amharic" else "Error: Timeout. Please try again."
        raise gr.Error(error_msg)
    except Exception as e:
        error_msg = f"ስህተት: ድምፅ መፍጠር አልተቻለም።\nError: {str(e)}" if language == "Amharic" else f"Error: Failed to generate audio.\nDetails: {str(e)}"
        raise gr.Error(error_msg)

def update_speakers(language):
    speakers = list(language_dict[language].keys())
    return gr.Dropdown(choices=speakers, value=speakers[0])

with gr.Blocks(title="Amharic & English TTS") as demo:
    gr.HTML("""
    <style>
        h1 { 
            color: #2E86C1; 
            text-align: center;
            background: linear-gradient(45deg, #FF007F, #2E86C1);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .gradio-button { 
            background: linear-gradient(45deg, #FF007F, #2E86C1) !important; 
            color: white !important; 
        }
        .gradio-textbox, .gradio-dropdown { 
            border-color: #2E86C1 !important; 
        }
    </style>
    <center><h1>Amharic & English Text-to-Speech</h1></center>
    """)

    with gr.Row():
        with gr.Column():
            language = gr.Dropdown(
                choices=["Amharic", "English"],
                value="Amharic",
                label="Select Language / ቋንቋ ይምረጡ"
            )
            input_text = gr.Textbox(
                lines=5, 
                label="Enter Text / ጽሑፍ ያስገቡ",
                placeholder="Type your text here... / ጽሑፍዎን ይጻፉ..."
            )
            speaker = gr.Dropdown(
                choices=["Ameha", "Mekdes"],
                value="Ameha",
                label="Select Speaker / አርቲስት ይምረጡ"
            )
            run_btn = gr.Button(value="Generate Audio / ድምፅ ፍጠር", variant="primary")

        with gr.Column():
            output_audio = gr.Audio(
                type="filepath",
                label="Generated Audio / የተፈጠረ ድምፅ"
            )

    language.change(
        update_speakers,
        inputs=language,
        outputs=speaker
    )

    run_btn.click(
        text_to_speech_edge,
        inputs=[input_text, language, speaker],
        outputs=output_audio
    )

if __name__ == "__main__":
    demo.launch(server_port=7860, share=False)
