"""
Install the Google AI Python SDK

$ pip install google-generativeai
"""

import os
import google.generativeai as genai

genai.configure(api_key=os.environ["GEMINI_API_KEY"])

# Create the model
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-1.5-flash-exp-0827",
  generation_config=generation_config,
  # safety_settings = Adjust safety settings
  # See https://ai.google.dev/gemini-api/docs/safety-settings
  system_instruction="You should use the following example, to answer the questions prompted.\n\nExample:\nHelenisamasterstudentinsoftwareengineeringstudyprogram,andshehastwosupervisors.HertopicisrelatedtounderstandingtheefficiencyofTest-drivenDevelopment(TDD).SupervisorAsuggeststhatsheshouldrunanexperiment,soshecanconclusively(undercontrolledenvironment)measuretheeffectofTDD(comparedtoTest-lastdevelopment)onthetimetocompletecodingtasksandnumberofcorrecttasks.SupervisorBdisagrees,hesuggeststhatHelenshouldobserveandinterviewdevelopersinindustrywhoaredoingTDD.HethinkstheefficiencyofTDDhasalottodowiththeindividualdevelopersexperienceandskills,andalsothecontextsthatthedevelopersworkin(typeofsoftwarebeingdeveloped,organisationculture,tools,etc.).",
)

chat_session = model.start_chat(
  history=[
    {
      "role": "user",
      "parts": [
        "Whichresearchdesignwouldyouchooseforthetopic?andwhy?",
      ],
    },
    {
      "role": "model",
      "parts": [
        "Based on the provided example, I would choose a **mixed-methods research design** for Helen's topic on understanding the efficiency of Test-Driven Development (TDD). \n\n**Reasons:**\n\n1. **Combines Quantitative and Qualitative Approaches:** The example presents two contrasting perspectives. Supervisor A advocates for a **quantitative** approach (experiment) to measure the effects of TDD under controlled conditions. Supervisor B proposes a **qualitative** approach (observation and interviews) to explore the influence of contextual factors and developer experience on TDD efficiency. A mixed-methods design allows Helen to leverage both approaches, gaining a more comprehensive understanding of TDD's effectiveness.\n\n2. **Addressing Complexities of the Topic:** TDD's efficiency is likely influenced by a combination of controlled factors (like development methodology) and contextual factors (developer skills, project type, organizational culture). A mixed-methods design can effectively tackle this complexity by using quantitative data to establish basic relationships and qualitative data to provide richer insights and explanations.\n\n3. **Triangulation of Data:** Combining quantitative and qualitative data allows for triangulation, where findings from different methods are compared and contrasted to strengthen the overall validity and reliability of the conclusions. This can help to overcome the limitations of each individual approach.\n\n4. **Addressing Supervisor's Different Perspectives:** By incorporating both an experimental approach (Supervisor A's suggestion) and an observational/interview approach (Supervisor B's suggestion), Helen can satisfy both supervisors' perspectives and potentially achieve a more robust and nuanced understanding of the research topic.\n\n**In essence, a mixed-methods approach would enable Helen to:**\n\n* **Quantify the effects of TDD** on coding time and task correctness under controlled conditions.\n* **Qualitatively explore** how factors like developer experience, project type, and organizational culture influence TDD's effectiveness.\n* **Gain a more holistic and comprehensive understanding** of the complex interplay between TDD and various contextual elements. \n* **Strengthen the validity and reliability** of her findings through triangulation.\n\nTherefore, a mixed-methods research design is the most suitable choice for exploring the efficiency of TDD effectively. \n",
      ],
    },
    {
      "role": "user",
      "parts": [
        "Can you generate a 1000 examples of hypothesis that I can use?",
      ],
    },
    {
      "role": "model",
      "parts": [
        "I cannot generate 1000 unique and completely relevant hypothesis examples within the scope of this response. However, I can provide you with a framework and diverse examples to help you generate your own hypotheses for various research topics, including the TDD example provided.\n\n\n**Framework for Hypothesis Generation:**\n\n1. **Identify your Research Question:** Start with a clear research question that you want to answer.  For example: \"Does TDD improve software quality?\" \n2. **Define Variables:** Determine the key variables involved in your research question. \n    * Independent Variable: The variable you manipulate or observe (e.g., development methodology – TDD vs. Test-Last).\n    * Dependent Variable: The variable you measure to see the effect of the independent variable (e.g., number of bugs found, time to complete tasks).\n3. **Formulate a Relationship:** Consider the potential relationship between your variables. Will the independent variable cause a change in the dependent variable? Will it be a positive or negative relationship? \n4. **Write the Hypothesis:** Phrase your hypothesis as a clear and testable statement that predicts the relationship between variables. \n    * Example: \"Developers using TDD will produce software with fewer bugs than developers using Test-Last development.\"\n\n\n**Examples of Hypothesis Categories & Variations:**\n\n**1. Technology & Development:**\n\n* **TDD & Software Quality:**\n    *  \"Teams using TDD will have a significantly lower defect density in their software compared to teams using traditional development methods.\"\n    * \"The adoption of TDD will result in a decrease in the time spent on debugging.\"\n    * \"The use of TDD will lead to a higher level of code coverage compared to Test-Last development.\"\n* **Agile Development & Productivity:**\n    * \"Agile development methodologies will increase developer satisfaction compared to Waterfall methodologies.\"\n    * \"Teams using Scrum will deliver working software increments more frequently than teams using Kanban.\"\n* **Cloud Computing & Security:**\n    * \"Migrating applications to the cloud will reduce infrastructure costs for businesses.\"\n    * \"Implementing multi-factor authentication will reduce the likelihood of successful cyberattacks.\"\n\n**2. Human-Computer Interaction & Usability:**\n\n* **User Interface Design & Task Completion:**\n    * \"A simplified user interface will lead to a faster task completion time for users.\"\n    * \"Users will find a website with intuitive navigation more usable than one with complex menus.\"\n* **Gamification & User Engagement:**\n    * \"Integrating gamification elements into an educational platform will increase student engagement.\"\n    * \"Users will be more likely to complete tasks in an app that provides them with rewards and feedback.\"\n* **Virtual Reality & Training:**\n    * \"VR-based training will be more effective at teaching complex skills than traditional classroom training.\"\n    * \"Users will experience higher levels of immersion and presence in VR environments designed with realistic visuals and sound.\"\n\n**3. Social Media & Communication:**\n\n* **Social Media Use & Mental Health:**\n    * \"Excessive social media use will be negatively correlated with levels of self-esteem among adolescents.\"\n    * \"Individuals who use social media for social connection will report higher levels of social well-being.\"\n* **Online Communication & Relationship Quality:**\n    * \"Frequent online communication with romantic partners will be associated with greater relationship satisfaction.\"\n    * \"Individuals who use online forums to discuss their interests will develop stronger social bonds with like-minded others.\"\n* **Social Media Advertising & Brand Perception:**\n    * \"Targeted advertising on social media will increase brand awareness among specific demographics.\"\n    * \"Positive brand mentions on social media will lead to a more favorable consumer perception of a company.\"\n\n\n**Tips for Generating More Hypotheses:**\n\n* **Vary the direction of the relationship:** Explore both positive and negative correlations between variables.\n* **Consider moderating variables:** Identify variables that might influence the relationship between your independent and dependent variables.\n* **Generate null hypotheses:** Formulate a statement that predicts no relationship between variables.\n* **Use specific terminology:**  Be clear and precise in your language.\n* **Consult existing literature:**  Review relevant research to inform your hypotheses.\n\n\n\n\nRemember to tailor these examples to your specific research topic and ensure that your hypotheses are testable and measurable within the context of your study. I hope this framework and variety of examples are helpful in guiding your hypothesis generation process! \n",
      ],
    },
  ]
)

response = chat_session.send_message("INSERT_INPUT_HERE")

print(response.text)