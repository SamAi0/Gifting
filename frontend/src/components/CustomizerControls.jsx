import React from 'react';
import { Type, Image as ImageIcon, Trash2, Palette, AlertCircle, RefreshCcw, Plus } from 'lucide-react';
import LogoUploader from './LogoUploader';

const CustomizerControls = ({ 
  textEntries, setTextEntries, 
  textColor, setTextColor, 
  logoFiles, setLogoFiles, 
  setLogoPreviews, 
  maxZones, 
  onReset, 
  warningMessage 
}) => {
  
  const updateTextEntry = (id, text) => {
    setTextEntries(prev => prev.map(entry => entry.id === id ? { ...entry, text } : entry));
  };

  const addTextEntry = () => {
    if (textEntries.length + logoFiles.length < maxZones) {
      setTextEntries(prev => [...prev, { id: Date.now(), text: '' }]);
    }
  };

  const removeTextEntry = (id) => {
    if (textEntries.length > 1) {
      setTextEntries(prev => prev.filter(entry => entry.id !== id));
    } else {
      updateTextEntry(id, '');
    }
  };

  const colorOptions = [
    { name: 'Black', value: '#000000', class: 'bg-black' },
    { name: 'White', value: '#FFFFFF', class: 'bg-white border-2 border-gray-300' },
    { name: 'Gold', value: '#ff9100ff', class: 'bg-yellow-500' },
  ];

  const totalUsed = textEntries.length + logoFiles.length;
  const remaining = maxZones - totalUsed;

  return (
    <div className="space-y-8">
      {/* 1. Branding Color */}
      <section className="space-y-4">
        <label className="text-xs font-black text-slate-400 uppercase tracking-widest flex items-center gap-2">
          <Palette size={14} className="text-primary" /> Branding Color
        </label>
        <div className="flex gap-4">
          {colorOptions.map((color) => (
            <button
              key={color.value}
              onClick={() => setTextColor(color.value)}
              className={`flex-1 py-3 px-4 rounded-2xl border-2 font-bold text-xs transition-all flex items-center justify-center gap-3 ${
                textColor === color.value
                  ? 'border-primary bg-primary/5 shadow-sm'
                  : 'border-slate-100 hover:border-slate-200 bg-slate-50/50'
              }`}
            >
              <span className={`w-5 h-5 rounded-lg ${color.class} shadow-sm`}></span>
              <span className="text-slate-600">{color.name}</span>
            </button>
          ))}
        </div>
      </section>

      {/* 2. Personalized Texts */}
      <section className="space-y-4">
        <div className="flex items-center justify-between">
          <label className="text-xs font-black text-slate-400 uppercase tracking-widest flex items-center gap-2">
            <Type size={14} className="text-primary" /> Personalized Text
          </label>
          {remaining > 0 && (
            <button 
              onClick={addTextEntry}
              className="text-[10px] font-black text-primary uppercase tracking-widest flex items-center gap-1 hover:opacity-80 transition-opacity"
            >
              <Plus size={12} /> Add Another Line
            </button>
          )}
        </div>
        
        <div className="space-y-3">
          {textEntries.map((entry, index) => (
            <div key={entry.id} className="relative group">
              <input
                type="text"
                value={entry.text}
                onChange={(e) => updateTextEntry(entry.id, e.target.value)}
                placeholder={index === 0 ? "Type your primary message..." : "Type additional message..."}
                className="w-full px-5 py-4 bg-slate-50 border-2 border-transparent focus:border-primary/20 focus:bg-white rounded-[1.25rem] outline-none transition-all font-medium text-slate-700 placeholder:text-slate-300 shadow-sm"
              />
              {textEntries.length > 1 && (
                <button 
                  onClick={() => removeTextEntry(entry.id)}
                  className="absolute right-4 top-1/2 -translate-y-1/2 p-2 text-slate-200 hover:text-red-500 opacity-0 group-hover:opacity-100 transition-all"
                >
                  <Trash2 size={16} />
                </button>
              )}
            </div>
          ))}
        </div>
      </section>

      {/* 3. Corporate Logos */}
      <section className="space-y-4">
        <label className="text-xs font-black text-slate-400 uppercase tracking-widest flex items-center gap-2">
          <ImageIcon size={14} className="text-primary" /> Corporate Logo
        </label>
        
        <LogoUploader 
          files={logoFiles} 
          onFilesChange={setLogoFiles} 
          onPreviewChange={(mainPreview, allPreviews) => setLogoPreviews(allPreviews)} 
        />
      </section>

      {warningMessage && (
        <div className="flex gap-3 p-4 bg-red-50 rounded-2xl border border-red-100 text-red-600 text-[11px] font-bold">
          <AlertCircle size={14} className="shrink-0" />
          <p>{warningMessage}</p>
        </div>
      )}

      {/* Footer Controls */}
      <div className="flex gap-4 pt-4">
        <button
          onClick={onReset}
          className="flex-1 px-6 py-4 bg-slate-100 text-slate-400 rounded-2xl flex items-center justify-center hover:bg-slate-200 hover:text-slate-500 transition-all active:scale-95 group"
        >
          <RefreshCcw size={18} className="group-hover:rotate-180 transition-transform duration-500" />
          <span className="ml-2 font-black text-xs uppercase tracking-widest">Reset All</span>
        </button>
      </div>

      <div className="p-5 bg-slate-50/50 rounded-[1.5rem] border border-slate-100 text-slate-500 text-[10px] leading-relaxed italic">
        <p className="flex items-center gap-2 mb-1 font-black uppercase tracking-widest not-italic text-slate-400">
          <AlertCircle size={12} /> Designer's Note
        </p>
        <p>This is a real-time visualization. Our expert design team will manually adjust the alignment and scaling to ensure a premium finish for your bulk order.</p>
      </div>
    </div>
  );
};

export default CustomizerControls;
