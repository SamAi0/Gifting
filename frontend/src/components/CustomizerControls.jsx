import { useState, useRef } from 'react';
import { Type, Image as ImageIcon, Trash2, Palette, AlertCircle, RefreshCcw, Plus, Pipette, MessageSquare, Layout, ShoppingBag } from 'lucide-react';
import LogoUploader from './LogoUploader';

const CustomizerControls = ({ 
  activeStep, setActiveStep,
  textEntries, setTextEntries, 
  textColor, setTextColor, 
  logoFiles, setLogoFiles, 
  setLogoPreviews, 
  placement, setPlacement,
  designInstructions, setDesignInstructions,
  maxZones, 
  onReset, 
  warningMessage 
}) => {
  const colorInputRef = useRef(null);
  const [showPicker, setShowPicker] = useState(false);

  const placementOptions = [
    { label: 'Front', value: 'Front' },
    { label: 'Back', value: 'Back' },
    { label: 'Both', value: 'Both sides' },
    { label: '360°', value: '360° view' },
  ];

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

  const totalUsed = textEntries.length + logoFiles.length;
  const remaining = maxZones - totalUsed;

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

  return (
    <div className="flex flex-col h-full">
      <div className="flex-1 space-y-6">
        {/* STEP 1: BRANDING */}
        {activeStep === 1 && (
          <div className="space-y-6 animate-in fade-in slide-in-from-right-4 duration-300">
            {/* Branding Color */}
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

              {showPicker && (
                <div className="absolute top-full right-0 mt-2 p-3 bg-white rounded-2xl border border-slate-200 shadow-xl z-50 animate-in fade-in slide-in-from-top-1 duration-200 w-64">
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
                  <input type="color" ref={colorInputRef} value={textColor} onChange={(e) => setTextColor(e.target.value)} className="hidden" />
                </div>
              )}
            </section>

            {/* Corporate Logos */}
            <section className="space-y-3">
              <label className="text-[10px] font-black text-slate-400 uppercase tracking-widest flex items-center gap-2">
                <ImageIcon size={12} className="text-primary" /> Corporate Logo
              </label>
              <LogoUploader files={logoFiles} onFilesChange={setLogoFiles} onPreviewChange={(mainPreview, allPreviews) => setLogoPreviews(allPreviews)} />
            </section>
          </div>
        )}

        {/* STEP 2: DESIGN */}
        {activeStep === 2 && (
          <div className="space-y-6 animate-in fade-in slide-in-from-right-4 duration-300">
            {/* Personalized Texts */}
            <section className="space-y-3">
              <div className="flex items-center justify-between">
                <label className="text-[10px] font-black text-slate-400 uppercase tracking-widest flex items-center gap-2">
                  <Type size={12} className="text-primary" /> Personalized Text
                </label>
                {remaining > 0 && (
                  <button onClick={addTextEntry} className="text-[10px] font-black text-primary uppercase tracking-widest flex items-center gap-1 hover:opacity-80 transition-opacity">
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
                      <button onClick={() => removeTextEntry(entry.id)} className="absolute right-3 top-1/2 -translate-y-1/2 p-1.5 text-slate-200 hover:text-red-500 opacity-0 group-hover:opacity-100 transition-all">
                        <Trash2 size={14} />
                      </button>
                    )}
                  </div>
                ))}
              </div>
            </section>

            {/* Print Placement */}
            <section className="space-y-3">
              <label className="text-[10px] font-black text-slate-400 uppercase tracking-widest flex items-center gap-2">
                <Layout size={12} className="text-primary" /> Print Placement
              </label>
              <div className="flex p-1 bg-slate-50 rounded-xl border border-slate-100 gap-1">
                {placementOptions.map((opt) => (
                  <button
                    key={opt.value}
                    onClick={() => setPlacement(opt.value)}
                    className={`flex-1 py-2 text-[10px] font-bold rounded-lg transition-all ${
                      placement === opt.value
                        ? 'bg-white text-primary shadow-sm border border-slate-100'
                        : 'text-slate-400 hover:text-slate-600'
                    }`}
                  >
                    {opt.label}
                  </button>
                ))}
              </div>
            </section>
          </div>
        )}

        {/* STEP 3: REVIEW */}
        {activeStep === 3 && (
          <div className="space-y-6 animate-in fade-in slide-in-from-right-4 duration-300">
            {/* Design Instructions */}
            <section className="space-y-3">
              <label className="text-[10px] font-black text-slate-400 uppercase tracking-widest flex items-center gap-2">
                <MessageSquare size={12} className="text-primary" /> Design Instructions
              </label>
              <textarea
                value={designInstructions}
                onChange={(e) => setDesignInstructions(e.target.value)}
                placeholder="Share design instruction here..."
                rows={4}
                className="w-full px-4 py-3 bg-slate-50 border border-slate-100 focus:border-primary/20 focus:bg-white rounded-xl outline-none transition-all text-xs font-medium text-slate-700 placeholder:text-slate-300 shadow-sm resize-none"
              />
            </section>

            {/* Design Summary */}
            <div className="p-5 bg-slate-50 rounded-[2rem] border border-slate-100 space-y-4">
               <h4 className="text-[10px] font-black text-slate-900 uppercase tracking-widest">Final Configuration</h4>
               <div className="space-y-3">
                  <div className="flex justify-between items-center pb-2 border-b border-slate-200/50">
                    <span className="text-[9px] text-slate-400 uppercase font-black tracking-tighter">Color</span>
                    <div className="flex items-center gap-2">
                      <div className="w-3 h-3 rounded-full border border-black/10" style={{ backgroundColor: textColor }}></div>
                      <span className="text-[10px] font-black text-slate-700 uppercase">{textColor}</span>
                    </div>
                  </div>
                  <div className="flex justify-between items-center pb-2 border-b border-slate-200/50">
                    <span className="text-[9px] text-slate-400 uppercase font-black tracking-tighter">Placement</span>
                    <span className="text-[10px] font-black text-slate-700 uppercase">{placement}</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-[9px] text-slate-400 uppercase font-black tracking-tighter">Zones Used</span>
                    <span className="text-[10px] font-black text-slate-700 uppercase">{totalUsed} / {maxZones}</span>
                  </div>
               </div>
            </div>

            <button
              onClick={() => document.getElementById('add-to-cart-btn')?.click()}
              className="w-full btn-primary py-4 text-[10px] shadow-2xl shadow-primary/30 flex items-center justify-center gap-3"
            >
              <ShoppingBag size={14} />
              Confirm Design & Add to Cart
            </button>
          </div>
        )}

        {warningMessage && (
          <div className="flex gap-3 p-3 bg-red-50 rounded-xl border border-red-100 text-red-600 text-[10px] font-bold">
            <AlertCircle size={12} className="shrink-0" />
            <p>{warningMessage}</p>
          </div>
        )}
      </div>

      {/* TOOLBAR CONTROLS */}
      <div className="flex gap-3 pt-6 border-t border-slate-100">
        {activeStep > 1 && (
          <button
            onClick={() => setActiveStep(prev => prev - 1)}
            className="flex-1 px-4 py-3 bg-slate-100 text-slate-600 rounded-xl font-bold text-[10px] uppercase tracking-widest hover:bg-slate-200 transition-all"
          >
            Back
          </button>
        )}
        
        {activeStep < 3 ? (
          <button
            onClick={() => setActiveStep(prev => prev + 1)}
            className="flex-[2] btn-primary py-3 text-[10px] shadow-lg shadow-primary/20"
          >
            Next Step
          </button>
        ) : (
          <button
            onClick={onReset}
            className="px-4 py-3 bg-slate-100 text-slate-400 rounded-xl hover:bg-slate-200 transition-all"
            title="Reset All"
          >
            <RefreshCcw size={14} />
          </button>
        )}
      </div>
    </div>
  );
};

export default CustomizerControls;
