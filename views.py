from venv import logger
from django.http import JsonResponse # type: ignore
from django.shortcuts import get_object_or_404, redirect, render # type: ignore
from django.contrib.auth import authenticate, login # type: ignore
import PyPDF2 # type: ignore
from gtts import gTTS # type: ignore
import os
from django.conf import settings # type: ignore

from textwrap import wrap


from TTS.api import TTS
from pydub import AudioSegment
from pydub.utils import which


from .models import SubjectMaterial  
AudioSegment.converter = which("ffmpeg")

# Create your views here.
def home(request):
    # SubjectMaterial.objects.all().delete()
    return render(request,'home.html')


def login_view(request):
    if request.method == 'POST':
        user_id = request.POST['userId']
        password = request.POST['password']
        if user_id =='001' and password =='svit@001':
            return redirect('list_pdfs')
        elif user_id =='101' and password =='svit@101':
            return render(request,'index.html')

    
    
    return render(request, 'login.html')

def about(request):
    return render(request, 'about.html')

def signup(request):
    return render(request, 'signup.html')


# Function to extract text from the PDF# Function to extract text from the PDF
def extract_text_from_pdf(pdf_file):
    try:
        with open(pdf_file, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            text = ""
            for page in reader.pages:
                text += page.extract_text()
            return text.strip()
    except Exception as e:
        logger.error(f"Error extracting text from PDF: {e}")
        return ""

# Function to convert PDF text to speech with reference audio
def pdf_to_cloned_voice(pdf_file, reference_audio_path, output_audio_path, tts_model="tts_models/multilingual/multi-dataset/your_tts"):
    text = extract_text_from_pdf(pdf_file)
    if not text:
        raise ValueError("No text extracted from the PDF.")
    
    tts = TTS(model_name=tts_model)
    chunks = wrap(text, 3000)  # Split text into manageable chunks

    # Initialize full audio output file
    temp_audio_files = []

    # Process each chunk
    for idx, chunk in enumerate(chunks):
        temp_audio_path = f"{output_audio_path}_part{idx}.mp3"  # Temporary path for each chunk
        try:
            # Convert each chunk to speech
            tts.tts_to_file(
                text=chunk,
                speaker_wav=reference_audio_path,
                language="en",
                file_path=temp_audio_path
            )
            temp_audio_files.append(temp_audio_path)  # Keep track of temporary audio files
        except Exception as e:
            logger.error(f"Error during TTS conversion: {e}")
            raise

    # Combine all temporary audio files into one
    try:
        with open(output_audio_path, 'wb') as f_out:
            for temp_audio in temp_audio_files:
                with open(temp_audio, 'rb') as f_in:
                    f_out.write(f_in.read())  # Append each chunk to the final audio file
                os.remove(temp_audio)  # Clean up the temporary file
    except Exception as e:
        logger.error(f"Error combining audio files: {e}")
        raise

#--------------------------------------------------------------------------------------------------------------------------------------
# Main function for handling the toc request
def toc(request):
    if request.method == "POST" and request.FILES.get('pdf'):
        pdf_file = request.FILES['pdf']

        # Ensure the target directory exists before saving the file
        pdf_dir = settings.MEDIA_ROOT
        if not os.path.exists(pdf_dir):
            os.makedirs(pdf_dir)

        # Save the uploaded PDF file
        pdf_path = os.path.join(pdf_dir, pdf_file.name)
        with open(pdf_path, 'wb') as f:
            for chunk in pdf_file.chunks():
                f.write(chunk)

        # Get the subject name from the form input
        subject_name = request.POST['name']
        # reference_audio_path = r"C:\Users\nithi\Downloads\MiniProject (back)\MiniProject\Voxventure\voice_clone\rm.wav"
        reference_audio_path = r"N:\MiniProject (3)\MiniProject (3)\MiniProject\Voxventure\voice_clone\Daniel.wav"

        # Check if the reference audio file exists
        if not os.path.exists(reference_audio_path):
            return JsonResponse({"error": "Reference audio file not found."}, status=400)

        # Define audio directory
        audio_dir = os.path.join(settings.MEDIA_ROOT, 'audios')
        if not os.path.exists(audio_dir):
            os.makedirs(audio_dir)

        # Ensure unique audio file name
        base_audio_name = f"{subject_name}.mp3"
        audio_path = os.path.join(audio_dir, base_audio_name)

        counter = 1
        while os.path.exists(audio_path):
            audio_path = os.path.join(audio_dir, f"{subject_name}{counter}.mp3")
            counter += 1

        try:
            # Convert the PDF to cloned voice audio
            pdf_to_cloned_voice(pdf_path, reference_audio_path, audio_path)
        except Exception as e:
            logger.error(f"Error during PDF to cloned voice conversion: {e}")
            return JsonResponse({"error": "An error occurred during conversion."}, status=500)

        # Save the data in the database (assuming you have a SubjectMaterial model)
        subject_material = SubjectMaterial(
            name=subject_name,
            pdf=pdf_file,  # Save the uploaded PDF
            audio=os.path.relpath(audio_path, settings.MEDIA_ROOT)  # Save the relative path of the audio
        )
        subject_material.save()

        # Send the audio file path as a response
        return render(request, 'toc.html', {"audio_path": os.path.relpath(audio_path, settings.MEDIA_ROOT)})

    return render(request, 'toc.html')


#---------------------------------------------------------------------------------------------------------------------------------------

# Main function for handling the software engineering request
def software_engineering(request):
    if request.method == "POST" and request.FILES.get('pdf'):
        pdf_file = request.FILES['pdf']

        # Ensure the target directory exists before saving the file
        pdf_dir = settings.MEDIA_ROOT
        if not os.path.exists(pdf_dir):
            os.makedirs(pdf_dir)

        # Save the uploaded PDF file
        pdf_path = os.path.join(pdf_dir, pdf_file.name)
        with open(pdf_path, 'wb') as f:
            for chunk in pdf_file.chunks():
                f.write(chunk)

        # Get the subject name from the form input
        subject_name = request.POST['name']
        # reference_audio_path = r"C:\Users\nithi\Downloads\MiniProject (back)\MiniProject\Voxventure\voice_clone\rm.wav"
        reference_audio_path = r"N:\MiniProject (3)\MiniProject (3)\MiniProject\Voxventure\voice_clone\srk.wav"
        

        # Check if the reference audio file exists
        if not os.path.exists(reference_audio_path):
            return JsonResponse({"error": "Reference audio file not found."}, status=400)

        # Define audio directory
        audio_dir = os.path.join(settings.MEDIA_ROOT, 'audios')
        if not os.path.exists(audio_dir):
            os.makedirs(audio_dir)

        # Ensure unique audio file name
        base_audio_name = f"{subject_name}.mp3"
        audio_path = os.path.join(audio_dir, base_audio_name)

        counter = 1
        while os.path.exists(audio_path):
            audio_path = os.path.join(audio_dir, f"{subject_name}{counter}.mp3")
            counter += 1

        try:
            # Convert the PDF to cloned voice audio
            pdf_to_cloned_voice(pdf_path, reference_audio_path, audio_path)
        except Exception as e:
            logger.error(f"Error during PDF to cloned voice conversion: {e}")
            return JsonResponse({"error": "An error occurred during conversion."}, status=500)

        # Save the data in the database (assuming you have a SubjectMaterial model)
        subject_material = SubjectMaterial(
            name=subject_name,
            pdf=pdf_file,  # Save the uploaded PDF
            audio=os.path.relpath(audio_path, settings.MEDIA_ROOT)  # Save the relative path of the audio
        )
        subject_material.save()

        # Send the audio file path as a response
        return render(request, 'software_engineering.html', {"audio_path": os.path.relpath(audio_path, settings.MEDIA_ROOT)})

    return render(request, 'software_engineering.html')


# -----------------------------------------------------------------------------------------------------------------------------------
# Main function for handling the cn request
def cn(request):
    if request.method == "POST" and request.FILES.get('pdf'):
        pdf_file = request.FILES['pdf']

        # Ensure the target directory exists before saving the file
        pdf_dir = settings.MEDIA_ROOT
        if not os.path.exists(pdf_dir):
            os.makedirs(pdf_dir)

        # Save the uploaded PDF file
        pdf_path = os.path.join(pdf_dir, pdf_file.name)
        with open(pdf_path, 'wb') as f:
            for chunk in pdf_file.chunks():
                f.write(chunk)

        # Get the subject name from the form input
        subject_name = request.POST['name']
        # reference_audio_path = r"C:\Users\nithi\Downloads\MiniProject (back)\MiniProject\Voxventure\voice_clone\cn.wav"
        reference_audio_path = r"N:\MiniProject (3)\MiniProject (3)\MiniProject\Voxventure\voice_clone\sadh.wav"

        # Check if the reference audio file exists
        if not os.path.exists(reference_audio_path):
            return JsonResponse({"error": "Reference audio file not found."}, status=400)

        # Define audio directory
        audio_dir = os.path.join(settings.MEDIA_ROOT, 'audios')
        if not os.path.exists(audio_dir):
            os.makedirs(audio_dir)

        # Ensure unique audio file name
        base_audio_name = f"{subject_name}.mp3"
        audio_path = os.path.join(audio_dir, base_audio_name)

        counter = 1
        while os.path.exists(audio_path):
            audio_path = os.path.join(audio_dir, f"{subject_name}{counter}.mp3")
            counter += 1

        try:
            # Convert the PDF to cloned voice audio
            pdf_to_cloned_voice(pdf_path, reference_audio_path, audio_path)
        except Exception as e:
            logger.error(f"Error during PDF to cloned voice conversion: {e}")
            return JsonResponse({"error": "An error occurred during conversion."}, status=500)

        # Save the data in the database (assuming you have a SubjectMaterial model)
        subject_material = SubjectMaterial(
            name=subject_name,
            pdf=pdf_file,  # Save the uploaded PDF
            audio=os.path.relpath(audio_path, settings.MEDIA_ROOT)  # Save the relative path of the audio
        )
        subject_material.save()

        # Send the audio file path as a response
        return render(request, 'cn.html', {"audio_path": os.path.relpath(audio_path, settings.MEDIA_ROOT)})

    return render(request, 'cn.html')

#-------------------------------------------------------------------------------------------------------------------------------------
# Main function for handling the rm request
def rm(request):
    if request.method == "POST" and request.FILES.get('pdf'):
        pdf_file = request.FILES['pdf']

        # Ensure the target directory exists before saving the file
        pdf_dir = settings.MEDIA_ROOT
        if not os.path.exists(pdf_dir):
            os.makedirs(pdf_dir)

        # Save the uploaded PDF file
        pdf_path = os.path.join(pdf_dir, pdf_file.name)
        with open(pdf_path, 'wb') as f:
            for chunk in pdf_file.chunks():
                f.write(chunk)

        # Get the subject name from the form input
        subject_name = request.POST['name']
        # reference_audio_path = r"C:\Users\nithi\Downloads\MiniProject (back)\MiniProject\Voxventure\voice_clone\rm.wav"
        reference_audio_path = r"N:\MiniProject (3)\MiniProject (3)\MiniProject\Voxventure\voice_clone\rm.wav"

        # Check if the reference audio file exists
        if not os.path.exists(reference_audio_path):
            return JsonResponse({"error": "Reference audio file not found."}, status=400)

        # Define audio directory
        audio_dir = os.path.join(settings.MEDIA_ROOT, 'audios')
        if not os.path.exists(audio_dir):
            os.makedirs(audio_dir)

        # Ensure unique audio file name
        base_audio_name = f"{subject_name}.mp3"
        audio_path = os.path.join(audio_dir, base_audio_name)

        counter = 1
        while os.path.exists(audio_path):
            audio_path = os.path.join(audio_dir, f"{subject_name}{counter}.mp3")
            counter += 1

        try:
            # Convert the PDF to cloned voice audio
            pdf_to_cloned_voice(pdf_path, reference_audio_path, audio_path)
        except Exception as e:
            logger.error(f"Error during PDF to cloned voice conversion: {e}")
            return JsonResponse({"error": "An error occurred during conversion."}, status=500)

        # Save the data in the database (assuming you have a SubjectMaterial model)
        subject_material = SubjectMaterial(
            name=subject_name,
            pdf=pdf_file,  # Save the uploaded PDF
            audio=os.path.relpath(audio_path, settings.MEDIA_ROOT)  # Save the relative path of the audio
        )
        subject_material.save()

        # Send the audio file path as a response
        return render(request, 'rm.html', {"audio_path": os.path.relpath(audio_path, settings.MEDIA_ROOT)})

    return render(request, 'rm.html')
#-----------------------------------------------------------------------------------------------------------------------------------

# Main function for handling the ai request
def ai(request):
    if request.method == "POST" and request.FILES.get('pdf'):
        pdf_file = request.FILES['pdf']

        # Ensure the target directory exists before saving the file
        pdf_dir = settings.MEDIA_ROOT
        if not os.path.exists(pdf_dir):
            os.makedirs(pdf_dir)

        # Save the uploaded PDF file
        pdf_path = os.path.join(pdf_dir, pdf_file.name)
        with open(pdf_path, 'wb') as f:
            for chunk in pdf_file.chunks():
                f.write(chunk)

        # Get the subject name from the form input
        subject_name = request.POST['name']
        # reference_audio_path = r"C:\Users\nithi\Downloads\MiniProject (back)\MiniProject\Voxventure\voice_clone\ai.wav"
        reference_audio_path = r"N:\MiniProject (3)\MiniProject (3)\MiniProject\Voxventure\voice_clone\ai.wav"

        # Check if the reference audio file exists
        if not os.path.exists(reference_audio_path):
            return JsonResponse({"error": "Reference audio file not found."}, status=400)

        # Define audio directory
        audio_dir = os.path.join(settings.MEDIA_ROOT, 'audios')
        if not os.path.exists(audio_dir):
            os.makedirs(audio_dir)

        # Ensure unique audio file name
        base_audio_name = f"{subject_name}.mp3"
        audio_path = os.path.join(audio_dir, base_audio_name)

        counter = 1
        while os.path.exists(audio_path):
            audio_path = os.path.join(audio_dir, f"{subject_name}{counter}.mp3")
            counter += 1

        try:
            # Convert the PDF to cloned voice audio
            pdf_to_cloned_voice(pdf_path, reference_audio_path, audio_path)
        except Exception as e:
            logger.error(f"Error during PDF to cloned voice conversion: {e}")
            return JsonResponse({"error": "An error occurred during conversion."}, status=500)

        # Save the data in the database (assuming you have a SubjectMaterial model)
        subject_material = SubjectMaterial(
            name=subject_name,
            pdf=pdf_file,  # Save the uploaded PDF
            audio=os.path.relpath(audio_path, settings.MEDIA_ROOT)  # Save the relative path of the audio
        )
        subject_material.save()

        # Send the audio file path as a response
        return render(request, 'ai.html', {"audio_path": os.path.relpath(audio_path, settings.MEDIA_ROOT)})

    return render(request, 'ai.html')
#-----------------------------------------------------------------------------------------------------------------------------


# View to list all PDFs
def list_pdfs(request):
    # Get all SubjectMaterials (uploaded PDFs)
    subject_materials = SubjectMaterial.objects.all()
    return render(request, 'list_pdfs.html', {'subject_materials': subject_materials})

def student_access(request, subject_id):
    # Fetch the SubjectMaterial instance by subject_id
    subject_material = get_object_or_404(SubjectMaterial, id=subject_id)

    # Construct full URLs for the PDF and audio files
    pdf_url = request.build_absolute_uri(subject_material.pdf.url)  # Full URL for the PDF file
    # Correct URL for the audio file
    audio_url = request.build_absolute_uri(subject_material.audio.url) if subject_material.audio else None

    # Debugging: Print the URLs
    materials = SubjectMaterial.objects.all()
    for material in materials:
        print(material.name, material.pdf.url, material.audio.url if material.audio else None)
    old_path = material.audio.path
    print("PDF URL:", pdf_url)
    print("Audio URL:", old_path)
    
    print(materials)


    for material in SubjectMaterial.objects.all():
        print(material.audio.url)
    # Return the response to the template
    return render(request, 'student_access.html', {
        'subject_material': subject_material,
        'pdf_url': pdf_url,
        'audio_url': audio_url
    })
