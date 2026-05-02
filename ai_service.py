import os
from google import genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_career_insights(career_name, scores, traits_mapping):
    """
    Calls the Gemini API to get personalized career insights based on the user's scores.
    If no API key is set, returns a generic fallback response.
    """
    api_key = os.environ.get("GEMINI_API_KEY")
    
    if not api_key:
        return generate_fallback_insights(career_name, scores, traits_mapping)
        
    try:
        # Initialize the GenAI client
        client = genai.Client(api_key=api_key)
        
        # Prepare the prompt
        score_details = "\n".join([f"- {trait}: {score}" for trait, score in zip(traits_mapping, scores)])
        
        prompt = f"""
You are an expert career counselor AI. Your student has just taken an assessment 
and our ML model has recommended they pursue a career as a "{career_name}".

Their assessment scores out of 100 are:
{score_details}

Write a short, encouraging 3-paragraph career analysis for them.
Paragraph 1: Briefly explain why this career is a great fit based on their highest scores.
Paragraph 2: Point out 1 or 2 areas they might need to improve upon to succeed in this role.
Paragraph 3: Provide a list of 3 to 4 "Required Skills" crucial for this career.
Paragraph 4: Provide an "Estimated Salary Range" and briefly describe the "Growth Trends" for this industry over the next decade.
Paragraph 5: Give a quick motivating closing statement.

Keep the tone professional, motivating, and speak directly to the student ("You have strong...").
Do not use markdown formatting like ** or #, just plain text paragraphs separated by newlines.
"""

        # Call the Gemini model (using gemini-2.5-flash as the standard fast text model)
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
        )
        
        if response.text:
            return response.text
        else:
            return generate_fallback_insights(career_name, scores, traits_mapping)
            
    except Exception as e:
        print(f"Gemini API Error: {e}")
        return generate_fallback_insights(career_name, scores, traits_mapping)

def generate_fallback_insights(career_name, scores, traits_mapping):
    """Fallback generator if Gemini API is unavailable."""
    
    # Simple logic to find highest and lowest scores
    score_dict = {t: s for t, s in zip(traits_mapping, scores)}
    sorted_scores = sorted(score_dict.items(), key=lambda x: x[1], reverse=True)
    
    highest_trait = sorted_scores[0][0]
    lowest_trait = sorted_scores[-1][0]
    
    insight = f"""Based on our local analysis, a career as a {career_name} aligns well with your profile. Your exceptionally strong foundation in {highest_trait} indicates you have the natural aptitude required for the core responsibilities of this field.

To maximize your potential in this domain, we recommend focusing some additional effort on developing your skills in {lowest_trait}. In the modern workplace, a well-rounded skill set often differentiates top performers from the rest.

Required Skills: Analytical Thinking, Domain Knowledge, Targeted Problem Solving.

Estimated Salary Range: $70,000 - $120,000+ per year (Varies heavily by region and experience).
Growth Trends: High demand expected over the next decade as digital transformation continues.

This path offers excellent growth opportunities and stability. Keep honing your strengths, and you will be well-positioned for a successful and fulfilling career ahead!"""
    
    return insight

# ==========================================
# RESUME BUILDER AI FUNCTIONS
# ==========================================

def generate_resume_content(data: dict) -> dict:
    """
    Calls Gemini AI to generate professional resume content.
    Takes a dict with name, target_role, education, experience, skills, location.
    Returns a dict with keys: objective, summary, strengths (list).
    Falls back gracefully if Gemini is unavailable.
    """
    api_key = os.environ.get("GEMINI_API_KEY")
    fallback = generate_resume_fallback(data)

    if not api_key:
        return fallback

    try:
        import json as _json
        client = genai.Client(api_key=api_key)

        prompt = f"""You are a professional resume writer AI. Given the following student's details, generate resume content.

Student Details:
- Name: {data.get('name', '')}
- Target Job Role: {data.get('target_role', '')}
- Education: {data.get('education', '')}
- Work / Internship Experience: {data.get('experience', '')}
- Skills: {data.get('skills', '')}
- Location: {data.get('location', '')}

Generate the following 3 things tailored specifically to the student's target role:
1. A strong, 1-sentence professional career objective statement.
2. A compelling 2-3 sentence professional summary paragraph.
3. Exactly 4 key professional strengths as concise bullet phrases.

IMPORTANT: Return ONLY a valid JSON object with no markdown formatting, no code fences, no extra text.
The JSON must use these exact keys:
{{"objective": "one powerful sentence here", "summary": "2-3 sentence paragraph here", "strengths": ["strength 1", "strength 2", "strength 3", "strength 4"]}}"""

        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
        )

        if response.text:
            text = response.text.strip()
            # Strip markdown code fences if the model wraps output
            if text.startswith("```"):
                parts = text.split("```")
                text = parts[1] if len(parts) > 1 else text
                if text.startswith("json"):
                    text = text[4:]
            text = text.strip()
            result = _json.loads(text)
            # Validate expected keys are present
            if "objective" in result and "summary" in result and "strengths" in result:
                return result

        return fallback

    except Exception as e:
        print(f"Resume AI Error: {e}")
        return fallback


def generate_resume_fallback(data: dict) -> dict:
    """Returns a reasonable offline resume content dict when Gemini is unavailable."""
    name = data.get("name", "You")
    role = data.get("target_role", "the desired position")
    return {
        "objective": (
            f"Motivated and dedicated professional seeking a {role} position "
            f"where I can apply my academic knowledge and skills to drive meaningful impact."
        ),
        "summary": (
            f"{name} is a driven individual with a solid academic background and a passion for "
            f"excellence in {role}. Known for a proactive attitude and strong problem-solving abilities, "
            f"{name} brings both technical depth and interpersonal skills to every challenge."
        ),
        "strengths": [
            "Strong analytical and critical thinking mindset",
            "Excellent verbal and written communication skills",
            "Adaptable and fast learner in dynamic environments",
            "Collaborative team player with natural leadership qualities",
        ]
    }


if __name__ == "__main__":
    # Test the fallback
    traits = ["Math", "Science", "English", "Aptitude", "Tech"]
    test_scores = [90, 85, 70, 95, 80]
    print(get_career_insights("Data Scientist", test_scores, traits))
