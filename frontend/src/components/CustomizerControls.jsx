import { useState, useRef } from 'react';
import { Type, Image as ImageIcon, Trash2, Palette, AlertCircle, RefreshCcw, Plus, Pipette } from 'lucide-react';
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
  const colorInputRef = useRef(null);
  const [showPicker, setShowPicker] = useState(false);

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

  const totalUsed = textEntries.length + logoFiles.length;
  const remaining = maxZones - totalUsed;
  
  const colorOptions = [
    { name: 'Black', value: '#000000' },
    { name: 'White', value: '#FFFFFF' },
    { name: 'Gold', value: '#ff9100' },
    { name: 'Silver', value: '#C0C0C0' },
    { name: 'Navy', value: '#000080' },
  ];

  const extendedColors = [
    '#000000', '#FFFFFF', '#ff9100', '#C0C0C0', '#000080', 
    '#DC143C', '#2E7D32', '#1565C0', '#6A1B9A', '#37474F',
    '#E65100', '#006064', '#BF360C', '#827717', '#1A237E',
    '#F44336', '#9C27B0', '#00BCD4', '#4CAF50', '#FFEB3B'
  ];

  const activePreset = colorOptions.find(c => c.value === textColor);
  const isCustomColor = !activePreset;

  return (
    <div className="space-y-6">
      {/* 1. Branding Color */}
      <section className="space-y-3 relative">
        <div className="flex items-center justify-between">
          <label className="text-[10px] font-black text-slate-400 uppercase tracking-widest flex items-center gap-2">
            <Palette size={12} className="text-primary" /> Branding Color
          </label>
          <button 
            onClick={() => setShowPicker(!showPicker)}
            className="text-[10px] font-bold text-primary uppercase tracking-widest hover:opacity-70 transition-opacity flex items-center gap-1"
          >
            <Pipette size={12} /> {showPicker ? 'Close Palette' : 'Choose Your Color'}
          </button>
        </div>

        <div className="flex items-center gap-2">
          {/* Presets Row */}
          <div className="flex items-center gap-2 p-1.5 bg-slate-50 rounded-2xl border border-slate-100">
            {colorOptions.map((color) => (
              <button
                key={color.value}
                onClick={() => {
                  setTextColor(color.value);
                  setShowPicker(false);
                }}
                title={color.name}
                className={`w-7 h-7 rounded-full transition-all flex items-center justify-center relative border border-black/5 ${
                  textColor === color.value ? 'ring-2 ring-primary ring-offset-2 scale-90' : 'hover:scale-110'
                }`}
                style={{ backgroundColor: color.value }}
              >
                {textColor === color.value && <div className={`w-1 h-1 rounded-full ${color.value === '#FFFFFF' ? 'bg-slate-300' : 'bg-white'}`}></div>}
              </button>
            ))}
          </div>

          <div className="h-6 w-px bg-slate-200 mx-1"></div>

          {/* Custom Picker Trigger */}
          <button
            onClick={() => setShowPicker(!showPicker)}
            className={`flex-1 flex items-center gap-3 px-4 py-2.5 rounded-2xl border-2 transition-all group ${
              isCustomColor || showPicker
                ? 'border-primary bg-primary/5 shadow-sm' 
                : 'border-slate-100 bg-white hover:border-slate-200'
            }`}
          >
            <div 
              className="w-5 h-5 rounded-lg shadow-inner border border-black/5" 
              style={{ backgroundColor: textColor }}
            ></div>
            <div className="flex flex-col items-start leading-none">
              <span className="text-[10px] font-black text-slate-400 uppercase tracking-tighter">Custom Color</span>
              <span className="text-xs font-bold text-slate-700 uppercase tracking-tight">{textColor}</span>
            </div>
          </button>
        </div>

        {/* Compact Color Palette Popover */}
        {showPicker && (
          <div className="absolute top-full left-0 mt-2 p-3 bg-white rounded-2xl border border-slate-200 shadow-xl z-50 animate-in fade-in slide-in-from-top-1 duration-200 w-64">
            <div className="flex items-center justify-between mb-2">
              <span className="text-[9px] font-black text-slate-400 uppercase tracking-widest">Select Shade</span>
              <button 
                onClick={() => colorInputRef.current.click()}
                className="p-1 rounded-md hover:bg-slate-50 text-primary transition-colors"
                title="Advanced Picker"
              >
                <Pipette size={10} />
              </button>
            </div>
            
            <div className="grid grid-cols-8 gap-1.5">
              {extendedColors.map((color) => (
                <button
                  key={color}
                  onClick={() => {
                    setTextColor(color);
                    setShowPicker(false);
                  }}
                  className={`w-6 h-6 rounded-md border transition-all hover:scale-110 ${
                    textColor === color ? 'border-primary ring-1 ring-primary ring-offset-1' : 'border-slate-100'
                  }`}
                  style={{ backgroundColor: color }}
                />
              ))}
            </div>

            <input 
              type="color" 
              ref={colorInputRef}
              value={textColor}
              onChange={(e) => setTextColor(e.target.value)}
              className="hidden"
            />
          </div>
        )}
      </section>

      {/* 2. Personalized Texts */}
      <section className="space-y-3">
        <div className="flex items-center justify-between">
          <label className="text-[10px] font-black text-slate-400 uppercase tracking-widest flex items-center gap-2">
            <Type size={12} className="text-primary" /> Personalized Text
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
        
        <div className="space-y-2">
          {textEntries.map((entry, index) => (
            <div key={entry.id} className="relative group">
              <input
                type="text"
                value={entry.text}
                onChange={(e) => updateTextEntry(entry.id, e.target.value)}
                placeholder={index === 0 ? "Primary message..." : "Secondary message..."}
                className="w-full px-4 py-3 bg-slate-50 border border-slate-100 focus:border-primary/20 focus:bg-white rounded-xl outline-none transition-all text-sm font-medium text-slate-700 placeholder:text-slate-300 shadow-sm"
              />
              {textEntries.length > 1 && (
                <button 
                  onClick={() => removeTextEntry(entry.id)}
                  className="absolute right-3 top-1/2 -translate-y-1/2 p-1.5 text-slate-200 hover:text-red-500 opacity-0 group-hover:opacity-100 transition-all"
                >
                  <Trash2 size={14} />
                </button>
              )}
            </div>
          ))}
        </div>
      </section>

      {/* 3. Corporate Logos */}
      <section className="space-y-3">
        <label className="text-[10px] font-black text-slate-400 uppercase tracking-widest flex items-center gap-2">
          <ImageIcon size={12} className="text-primary" /> Corporate Logo
        </label>
        
        <LogoUploader 
          files={logoFiles} 
          onFilesChange={setLogoFiles} 
          onPreviewChange={(mainPreview, allPreviews) => setLogoPreviews(allPreviews)} 
        />
      </section>

      {warningMessage && (
        <div className="flex gap-3 p-3 bg-red-50 rounded-xl border border-red-100 text-red-600 text-[10px] font-bold">
          <AlertCircle size={12} className="shrink-0" />
          <p>{warningMessage}</p>
        </div>
      )}

      {/* Footer Controls */}
      <div className="flex gap-3 pt-2">
        <button
          onClick={onReset}
          className="flex-1 px-4 py-3 bg-slate-100 text-slate-400 rounded-xl flex items-center justify-center hover:bg-slate-200 hover:text-slate-500 transition-all active:scale-95 group"
        >
          <RefreshCcw size={14} className="group-hover:rotate-180 transition-transform duration-500" />
          <span className="ml-2 font-black text-[10px] uppercase tracking-widest">Reset All</span>
        </button>
      </div>

      <div className="p-4 bg-slate-50/50 rounded-2xl border border-slate-100 text-slate-500 text-[9px] leading-relaxed italic">
        <p className="flex items-center gap-2 mb-1 font-black uppercase tracking-widest not-italic text-slate-400">
          <AlertCircle size={10} /> Designer's Note
        </p>
        <p>This is a real-time visualization. Our team will manually optimize alignment for your bulk order.</p>
      </div>
    </div>
  );
};

export default CustomizerControls;
