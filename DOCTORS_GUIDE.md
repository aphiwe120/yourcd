# Medical Coding Assistant - Doctor's Guide

## Welcome! 👨‍⚕️👩‍⚕️

This tool helps you quickly find the correct **ICD-10 diagnostic codes** for your patients' diagnoses using **Artificial Intelligence**.

---

## 🎯 How to Use (Simple Steps)

### Step 1: Open the Application
Go to: **http://localhost:8000**

You'll see a clean, medical interface with a search box.

### Step 2: Describe the Diagnosis
In the text box labeled **"Describe the patient's diagnosis or symptoms:"**, type your clinical notes in plain language.

**Examples:**
- "Type 2 diabetes mellitus with hypertension and obesity"
- "Acute pneumonia due to bacterial infection"
- "Recurrent migraine headaches with aura"
- "Acute myocardial infarction of anterior wall"

### Step 3: Click "Search Codes"
The system will search its database of **41,008 ICD-10 codes** and return the best matches.

### Step 4: Review the Results
You'll see:
- **Code**: The ICD-10 code (e.g., J15.9)
- **Description**: Short description of the code
- **Definition**: Full WHO medical definition

### Step 5: Select Your Code
Choose the most appropriate code for your patient's diagnosis and use it in their medical record.

---

## 💡 Tips for Best Results

### Be Specific
❌ **Bad:** "Fever"  
✅ **Good:** "High fever lasting 5 days with cough and shortness of breath"

### Include Clinical Details
- **Patient age or age group**: "Elderly patient with..."
- **Duration**: "Chronic cough for 3 months"
- **Severity**: "Severe headache", "Mild arthritis"
- **Associated symptoms**: "Fever with nausea and vomiting"
- **Comorbidities**: "Diabetic with pneumonia"

### Use Medical Terminology
The AI understands both:
- Medical terms: "Pneumonia", "Myocardial infarction"
- Plain language: "Lung infection", "Heart attack"

---

## 📋 Common Diagnosis Examples

### Respiratory
- Acute bronchitis with fever
- Community-acquired pneumonia
- Chronic obstructive pulmonary disease (COPD)
- Persistent dry cough lasting 2 weeks
- Acute asthma exacerbation

### Cardiovascular
- Hypertension stage 2
- Acute myocardial infarction (heart attack)
- Heart failure with reduced ejection fraction
- Arrhythmia - irregular heartbeat
- Deep vein thrombosis (DVT)

### Metabolic
- Type 2 diabetes mellitus
- Obesity BMI > 35
- Hyperlipidemia (high cholesterol)
- Hypothyroidism
- Metabolic syndrome

### Infectious
- Acute urinary tract infection
- Gastroenteritis (food poisoning)
- Influenza (flu)
- Viral hepatitis
- Cellulitis (skin infection)

### Neurological
- Migraine with aura
- Generalized anxiety disorder
- Major depressive disorder
- Seizure disorder (epilepsy)
- Vertigo/dizziness

### Musculoskeletal
- Osteoarthritis of knee
- Lower back pain (lumbar strain)
- Rotator cuff tear
- Neck pain (cervical strain)
- Rheumatoid arthritis

---

## ⚠️ Important Notes for Doctors

### Code Accuracy
✅ This AI system suggests codes based on **41,008 verified ICD-10 codes**  
✅ All codes are from the **South African Master Industry Table (2021)**  
✅ The system ensures codes are clinically valid

### Your Responsibility
⚠️ **You** are responsible for selecting the final code  
⚠️ Always review the code definition carefully  
⚠️ Ensure the code matches your clinical documentation  
⚠️ Use your clinical judgment if the code doesn't feel right

### When to Verify Manually
- Complex or rare diagnoses
- Patients with multiple comorbidities requiring specific sequencing
- If you're unsure about the suggested code
- For South African PMB (Prescribed Minimum Benefit) codes

---

## 🔍 Search Examples by Department

### Emergency Department
- "Acute chest pain with EKG changes"
- "Head injury with altered consciousness"
- "Severe abdominal pain and vomiting"
- "Shortness of breath and tachycardia"

### Primary Care / General Practice
- "Patient with cough lasting 3 weeks"
- "New onset hypertension"
- "Routine diabetes follow-up"
- "Recurrent sinusitis"

### Cardiology
- "Acute coronary syndrome"
- "Heart failure, NYHA class 3"
- "Persistent atrial fibrillation"
- "Aortic valve stenosis"

### Orthopedics
- "Fracture of tibia with displacement"
- "Chronic knee pain from osteoarthritis"
- "Acute rotator cuff injury"
- "Herniated lumbar disc with radiculopathy"

### Pediatrics
- "Acute otitis media with effusion"
- "Febrile seizure in toddler"
- "Asthma exacerbation in child"
- "Failure to thrive"

### Oncology
- "Breast cancer, stage 3A"
- "Metastatic lung cancer"
- "Lymphoma in remission"
- "Cancer-related pain management"

---

## ❓ Frequently Asked Questions

**Q: How accurate is this system?**  
A: The system searches 41,008 verified ICD-10 codes. Accuracy is high for common diagnoses. Always verify the suggested code matches your clinical assessment.

**Q: Can I use this for billing?**  
A: Yes, but ensure the code is accurate for your patient's condition. Medical schemes require accurate coding.

**Q: What if the code I need isn't suggested?**  
A: Try rewording your description. The AI responds to different phrasings of the same condition.

**Q: Does this replace my medical judgment?**  
A: No! This is a suggestion tool. Your clinical judgment and documentation must guide the final code selection.

**Q: Is my patient data secure?**  
A: This system only processes your diagnostic descriptions. No patient identifiable information is stored. The search is local to your facility.

**Q: What's the difference between suggested codes?**  
A: Different codes represent different aspects of the same condition (severity, specificity, laterality, etc.). Choose the most specific one for your clinical situation.

---

## 🚀 Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| **Tab** | Move between fields |
| **Enter** | Submit search (from text box) |
| **Ctrl+A** | Select all text in search box |

---

## 📞 Need Help?

### Technical Issues
- **Server not responding**: Check internet connection
- **Codes not loading**: Refresh your browser (F5)
- **Slow search**: Try a simpler description

### Clinical Questions
- Refer to [ICD-10 Official Code List](https://www.who.int/standards/classifications/classification-of-diseases)
- Check your hospital's ICD-10 coding guidelines
- Consult with your coding department

---

## 🎓 Learning ICD-10 Structure

ICD-10 codes have this structure:  
**[Letter][2 digits].[1 digit].[1 optional digit]**

Example: **J15.9**
- **J** = Chapter (Respiratory diseases)
- **15** = Category (Bacterial pneumonia)
- **9** = Unspecified/Other specification

The AI suggests the most specific code available for your description.

---

## 📊 Database Information

**Records Available**: 41,008  
**Data Source**: South African ICD-10 Master Industry Table (2021)  
**Updates**: Check with your IT department for latest versions  
**Validation**: All codes validated against South African medical scheme requirements

---

## ✅ Checklist Before Finalizing a Code

Before you use a suggested code:

- [ ] Does the code match the patient's documented diagnosis?
- [ ] Have you reviewed the full code definition?
- [ ] Is this the most specific code available?
- [ ] Does this code have any age/gender restrictions that don't apply?
- [ ] Is this code acceptable to your medical scheme (PMB compliant)?
- [ ] Have you documented the clinical reasoning in the patient record?

---

## 🎯 Your Benefits

✅ **Speed**: Find codes in seconds instead of minutes  
✅ **Accuracy**: Avoid coding errors and claim rejections  
✅ **Learning**: Discover alternative codes and ICD-10 structure  
✅ **Efficiency**: Spend more time on patient care  
✅ **Revenue**: Reduce claim denials due to incorrect coding  

---

## 📝 Feedback

Your feedback helps us improve this tool:
- Codes that were difficult to find
- Suggestions for better descriptions
- Technical issues

Share with: [Your IT Department / Medical Records]

---

**Last Updated**: 2024-11-17  
**Version**: 1.0  
**Status**: Production Ready

**Welcome to faster, smarter medical coding!** 🏥✨
