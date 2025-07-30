import tempfile
import edge_tts
import gradio as gr
import asyncio

# Using the exact voices from your README for consistency
language_dict = {
    "Amharic": {
        "Ameha": "am-ET-AmehaNeural",
        "Mekdes": "am-ET-MekdesNeural"
    },
    "English": {
        "Ryan (UK Male)": "en-GB-RyanNeural",
        "Clara (CA Female)": "en-CA-ClaraNeural"
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
        error_msg = "Error: Timeout. Please try again. (ስህተት: ጊዜ አልቋል)"
        raise gr.Error(error_msg)
    except Exception as e:
        error_msg = f"Error: Could not generate audio.\n{str(e)}"
        raise gr.Error(error_msg)

def update_speaker_choices(language):
    speakers = list(language_dict[language].keys())
    return gr.Dropdown(choices=speakers, value=speakers[0])

with gr.Blocks(title="TTS", theme=gr.themes.Soft()) as demo:
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
    </style>
    <center>
        <h1>Amharic & English Text-to-Speech</h1>
    </center>
    """)

    with gr.Row():
        with gr.Column(scale=1):
            input_text = gr.Textbox(
                lines=5, 
                label="ጽሑፍ ያስገቡ / Enter Text",
                placeholder="Type your text here to generate audio..."
            )
            
            language_selector = gr.Dropdown(
                choices=list(language_dict.keys()),
                value="Amharic",
                label="ቋንቋ ይምረጡ / Select Language"
            )

            speaker_selector = gr.Dropdown(
                choices=list(language_dict["Amharic"].keys()),
                value="Ameha",
                label="ድምፁን የሚያሰማ / Voice"
            )
            
            run_btn = gr.Button(
                value="ድምፅ ፍጠር / Generate Audio", 
                variant="primary",
                scale=1
            )

        with gr.Column(scale=1):
            output_audio = gr.Audio(
                type="filepath",
                label="የተፈጠረ ድምፅ / Generated Audio",
                elem_classes="output-audio"
            )

    language_selector.change(
        fn=update_speaker_choices,
        inputs=language_selector,
        outputs=speaker_selector
    )
    
    run_btn.click(
        text_to_speech_edge,
        inputs=[input_text, language_selector, speaker_selector],
        outputs=output_audio
    )

if __name__ == "__main__":
    demo.launch(server_port=7860, share=False)
