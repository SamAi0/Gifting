import React, { useState, useRef, useCallback } from 'react';
import { Upload, X, FileText, File as FileIcon, AlertCircle, CheckCircle2, Info } from 'lucide-react';

const LogoUploader = ({ files, onFilesChange, onPreviewChange }) => {
  const [dragActive, setDragActive] = useState(false);
  const [error, setError] = useState('');
  const inputRef = useRef(null);

  const ACCEPTED_FORMATS = [
    '.pdf', '.ai', '.psd', '.cdr', '.png', '.jpeg', '.jpg', '.tiff', '.tif', '.bmp'
  ];
  
  const MAX_FILE_SIZE = 10 * 1024 * 1024; // 10MB
  const MAX_TOTAL_SIZE = 100 * 1024 * 1024; // 100MB

  const validateFiles = (newFiles) => {
    let validFiles = [];
    let totalSize = files.reduce((acc, f) => acc + f.size, 0);
    let errorMessage = '';

    for (const file of newFiles) {
      const extension = '.' + file.name.split('.').pop().toLowerCase();
      
      if (!ACCEPTED_FORMATS.includes(extension)) {
        errorMessage = `Format ${extension} is not supported.`;
        continue;
      }

      if (file.size > MAX_FILE_SIZE) {
        errorMessage = `File ${file.name} exceeds 10MB limit.`;
        continue;
      }

      if (totalSize + file.size > MAX_TOTAL_SIZE) {
        errorMessage = 'Total upload size exceeds 100MB.';
        break;
      }

      validFiles.push(file);
      totalSize += file.size;
    }

    if (errorMessage) {
      setError(errorMessage);
      setTimeout(() => setError(''), 5000);
    }

    return validFiles;
  };

  const handleFiles = (incomingFiles) => {
    const validNewFiles = validateFiles(Array.from(incomingFiles));
    if (validNewFiles.length > 0) {
      const updatedFiles = [...files, ...validNewFiles];
      onFilesChange(updatedFiles);
      
      // Update preview with the first image file if available
      updatePreview(updatedFiles);
    }
  };

  const updatePreview = async (allFiles) => {
    const imageFiles = allFiles.filter(f => 
      ['.png', '.jpeg', '.jpg', '.bmp'].includes('.' + f.name.split('.').pop().toLowerCase())
    );
    
    if (imageFiles.length === 0) {
      onPreviewChange(null, []);
      return;
    }

    const previewPromises = imageFiles.map(file => {
      return new Promise((resolve) => {
        const reader = new FileReader();
        reader.onload = (e) => resolve(e.target.result);
        reader.readAsDataURL(file);
      });
    });

    const allPreviews = await Promise.all(previewPromises);
    onPreviewChange(allPreviews[0], allPreviews);
  };

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFiles(e.dataTransfer.files);
    }
  };

  const handleChange = (e) => {
    e.preventDefault();
    if (e.target.files && e.target.files[0]) {
      handleFiles(e.target.files);
    }
  };

  const removeFile = (index) => {
    const updatedFiles = files.filter((_, i) => i !== index);
    onFilesChange(updatedFiles);
    updatePreview(updatedFiles);
  };

  const formatSize = (bytes) => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  const getFileIcon = (fileName) => {
    const ext = fileName.split('.').pop().toLowerCase();
    if (['png', 'jpg', 'jpeg', 'bmp'].includes(ext)) return <FileIcon size={18} className="text-blue-500" />;
    if (['pdf', 'ai', 'psd', 'cdr'].includes(ext)) return <FileText size={18} className="text-orange-500" />;
    return <FileIcon size={18} className="text-gray-400" />;
  };

  return (
    <div className="space-y-6">
      <div 
        className={`relative group border-2 border-dashed rounded-3xl p-8 transition-all duration-300 flex flex-col items-center justify-center cursor-pointer
          ${dragActive ? 'border-primary bg-primary/5 scale-[1.01]' : 'border-slate-200 hover:border-primary/40 hover:bg-slate-50/50'}`}
        onDragEnter={handleDrag}
        onDragLeave={handleDrag}
        onDragOver={handleDrag}
        onDrop={handleDrop}
        onClick={() => inputRef.current.click()}
      >
        <input
          ref={inputRef}
          type="file"
          multiple
          className="hidden"
          accept={ACCEPTED_FORMATS.join(',')}
          onChange={handleChange}
        />
        
        <div className="w-16 h-16 rounded-2xl bg-primary/10 flex items-center justify-center text-primary mb-4 group-hover:scale-110 transition-transform">
          <Upload size={32} />
        </div>
        
        <h3 className="text-lg font-bold text-slate-900 mb-1">Click or Drag & Drop to Upload</h3>
        <p className="text-xs text-slate-400 font-medium text-center max-w-xs">
          Supported formats: .pdf, .ai, .psd, .cdr, .png, .jpeg, .jpg, .tiff, .tif, .bmp
        </p>
        
        {dragActive && (
          <div className="absolute inset-0 rounded-3xl bg-primary/10 backdrop-blur-[2px] flex items-center justify-center z-10 pointer-events-none border-2 border-primary">
            <p className="text-primary font-bold flex items-center gap-2">
              <Upload size={24} /> Drop files here
            </p>
          </div>
        )}
      </div>

      {/* Error Message */}
      {error && (
        <div className="flex items-center gap-2 p-4 bg-red-50 rounded-2xl border border-red-100 text-red-600 text-sm animate-shake">
          <AlertCircle size={18} className="shrink-0" />
          <p className="font-bold">{error}</p>
        </div>
      )}

      {/* File List */}
      {files.length > 0 && (
        <div className="space-y-3">
          <div className="flex justify-between items-center px-2">
            <h4 className="text-sm font-bold text-slate-700 uppercase tracking-wider">Uploaded Files ({files.length})</h4>
            <span className="text-[10px] font-black text-slate-400">TOTAL: {formatSize(files.reduce((acc, f) => acc + f.size, 0))}</span>
          </div>
          <div className="grid gap-3">
            {files.map((file, index) => (
              <div 
                key={`${file.name}-${index}`}
                className="flex items-center gap-4 p-4 bg-white border border-slate-100 rounded-2xl shadow-sm group hover:border-primary/20 hover:shadow-md transition-all"
              >
                <div className="w-10 h-10 rounded-xl bg-slate-50 flex items-center justify-center">
                  {getFileIcon(file.name)}
                </div>
                <div className="flex-1 min-w-0">
                  <p className="text-sm font-bold text-slate-900 truncate">{file.name}</p>
                  <p className="text-[10px] text-slate-400 font-medium">{formatSize(file.size)}</p>
                </div>
                <button 
                  onClick={(e) => {
                    e.stopPropagation();
                    removeFile(index);
                  }}
                  className="w-8 h-8 rounded-lg flex items-center justify-center text-slate-300 hover:text-red-500 hover:bg-red-50 transition-all"
                >
                  <X size={18} />
                </button>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Guidelines */}
      <div className="pt-6 border-t border-slate-100">
        <h4 className="text-sm font-bold text-slate-900 mb-4 flex items-center gap-2">
          <Info size={16} className="text-primary" /> Guidelines
        </h4>
        <ul className="space-y-3">
          {[
            'Upload the correct quantity of photos according to the selected specification to avoid quantity mismatch.',
            'Share high-resolution images to ensure clear and sharp prints; low-resolution images may appear blurry or pixelated.',
            'Text cannot be added to the print file due to design restrictions.',
            'If the shared images are not suitable for the chosen specification, white borders may be added to the print file to ensure the best possible outcome.',
            'Please select your image files or zip archive accordingly: max. 10 MB per file and max. 100 MB for full/total uploads.'
          ].map((point, i) => (
            <li key={i} className="flex gap-3 text-xs text-slate-500 leading-relaxed">
              <span className="text-primary font-bold mt-0.5">•</span>
              {point}
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
};

export default LogoUploader;
