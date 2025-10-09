// App.jsx
import { useState } from "react";
import { Briefcase } from "lucide-react";
import FileUploader from "./components/FileUploader";
import JobDescriptionInput from "./components/JobDescriptionInput";
import ResultsTable from "./components/ResultsTable";
import { uploadAndRankResumes } from "./api";

function App() {
  const [files, setFiles] = useState([]);
  const [jobDescription, setJobDescription] = useState("");
  const [jdSkills, setJdSkills] = useState("");
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async () => {
    if (!files.length || !jobDescription.trim()) {
      alert("Please upload resumes and enter a job description");
      return;
    }
    setLoading(true);

    const formData = new FormData();
    formData.append("job_description", jobDescription);
    formData.append("jd_skills", jdSkills);
    files.forEach((file) => formData.append("files", file));

    try {
      const ranked = await uploadAndRankResumes(formData);
      setResults(ranked);
    } catch (err) {
      alert("Error ranking resumes. Please try again.");
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

 return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100 py-8 px-4 sm:px-6 lg:px-8">
      <div className="max-w-5xl mx-auto">
        {/* Header */}
        <div className="bg-white rounded-xl shadow-md border border-slate-200 p-8 mb-8 text-center">
          <div className="flex items-center justify-center mb-3">
            <Briefcase className="w-10 h-10 text-indigo-600 mr-3" />
            <h1 className="text-3xl sm:text-4xl font-bold text-slate-900">
              Smart-Hire: Resume Ranking System
            </h1>
          </div>
          <p className="text-center text-slate-600 max-w-2xl mx-auto">
            Upload candidate resumes and match them against your job requirements
          </p>
        </div>

        {/* Main Content */}
        <div className="bg-white rounded-xl shadow-md border border-slate-200 p-8 sm:p-10 max-w-5xl mx-auto">
          <div className="space-y-8">
            <FileUploader onFilesChange={setFiles} files={files} />
            <div className="border-t border-slate-200">
              <JobDescriptionInput
                jobDescription={jobDescription}
                jdSkills={jdSkills}
                setJobDescription={setJobDescription}
                setJdSkills={setJdSkills}
              />
            </div>

            <button
              onClick={handleSubmit}
              disabled={loading || !files.length || !jobDescription.trim()}
              className="w-full py-4 px-6 bg-indigo-600 text-white font-semibold text-lg rounded-lg hover:bg-indigo-700 disabled:bg-slate-300 disabled:cursor-not-allowed focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 transition-colors duration-200 shadow-sm"
            >
              {loading ? (
                <span className="flex items-center justify-center">
                  <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  Analyzing Resumes...
                </span>
              ) : (
                "Rank Resumes"
              )}
            </button>
          </div>

          <ResultsTable results={results} />
        </div>

        {/* Footer */}
        <div className="text-center mt-8 text-sm text-slate-500">
          <p>Powered by AI-driven candidate matching technology</p>
        </div>
      </div>
    </div>
  );
}

export default App;