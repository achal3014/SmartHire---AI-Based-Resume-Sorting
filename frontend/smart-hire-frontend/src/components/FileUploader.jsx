// FileUploader.jsx
import { useState } from "react";
import { Upload, FileText } from "lucide-react";

const FileUploader = ({ onFilesChange, files }) => {
  const [dragging, setDragging] = useState(false);

  const handleFiles = (fileList) => {
    const fileArray = Array.from(fileList);
    onFilesChange(fileArray);
  };

  return (
    <div className="space-y-10 pt-6 pb-8"> {/* Increased overall vertical padding */}
      <label className="block text-lg font-semibold text-slate-700 mb-3">
        Upload Resumes
      </label>

      <div
        className={`border-2 border-dashed rounded-xl px-16 py-24 text-center cursor-pointer transition-all duration-200 ${
          dragging
            ? "border-indigo-500 bg-indigo-50"
            : "border-slate-300 bg-slate-50 hover:border-slate-400"
        }`}
        style={{ minHeight: "280px" }} // slightly taller
        onDragOver={(e) => {
          e.preventDefault();
          setDragging(true);
        }}
        onDragLeave={() => setDragging(false)}
        onDrop={(e) => {
          e.preventDefault();
          setDragging(false);
          handleFiles(e.dataTransfer.files);
        }}
        onClick={() => document.getElementById("file-input").click()}
      >
        <Upload className="w-12 h-12 mx-auto mb-8 text-slate-400" />
        <p className="text-slate-700 font-semibold mb-3 text-lg">
          Drag and drop resume files here
        </p>
        <p className="text-slate-500 mb-4">or click to browse</p>
        <p className="text-sm text-slate-400">
          Supports PDF, DOC, DOCX , TXT formats
        </p>

        <input
          id="file-input"
          type="file"
          multiple
          onChange={(e) => handleFiles(e.target.files)}
          className="hidden"
          accept=".pdf,.doc,.docx"
        />
      </div>

      {files.length > 0 && (
        <div className="bg-slate-50 rounded-lg p-5 border border-slate-200">
          <p className="text-base font-semibold text-slate-700 mb-3">
            {files.length} file(s) selected
          </p>
          <div className="space-y-2">
            {files.map((file, idx) => (
              <div key={idx} className="flex items-center text-sm text-slate-600">
                <FileText className="w-4 h-4 mr-2 text-slate-400" />
                {file.name}
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default FileUploader;
