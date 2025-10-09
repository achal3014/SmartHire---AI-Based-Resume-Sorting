// JobDescriptionInput.jsx

const JobDescriptionInput = ({
  jobDescription,
  jdSkills,
  setJobDescription,
  setJdSkills,
}) => (
  <div className="py-6 px-4 space-y-10 max-w-4xl mx-auto"> {/* Matches FileUploader layout */}
    <div>
      <label className="block text-xl font-semibold text-slate-800 mb-4 text-left">
        Job Description
      </label>

      <div className="border-2 border-slate-300 rounded-xl bg-slate-50 hover:border-slate-400 transition-all duration-200 p-8">
        <textarea
          className="w-full h-44 px-6 py-5 border border-slate-200 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none resize-none text-slate-700 text-base leading-relaxed bg-white placeholder:text-slate-400"
          placeholder="Enter the complete job description including responsibilities, qualifications, and requirements..."
          value={jobDescription}
          onChange={(e) => setJobDescription(e.target.value)}
        />
      </div>
    </div>

    <div>
      <label className="block text-xl font-semibold text-slate-800 mb-4 text-left">
        Required Skills
      </label>

      <div className="border-2 border-slate-300 rounded-xl bg-slate-50 hover:border-slate-400 transition-all duration-200 p-8">
        <input
          type="text"
          className="w-full h-16 px-6 py-5 border border-slate-200 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none text-slate-700 text-base bg-white placeholder:text-slate-400"
          placeholder="E.g., React, Node.js, Python, SQL, Project Management"
          value={jdSkills}
          onChange={(e) => setJdSkills(e.target.value)}
        />
        <p className="text-sm text-slate-500 mt-3">
          Separate multiple skills with commas
        </p>
      </div>
    </div>
  </div>
);

export default JobDescriptionInput;
