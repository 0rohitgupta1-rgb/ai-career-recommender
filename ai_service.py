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

if __name__ == "__main__":
    # Test the fallback
    traits = ["Math", "Science", "English", "Aptitude", "Tech"]
    test_scores = [90, 85, 70, 95, 80]
    print(get_career_insights("Data Scientist", test_scores, traits))
