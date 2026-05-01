import { Type, AlertCircle, RefreshCcw, Image as ImageIcon, X, Palette } from 'lucide-react';

const CustomizerControls = ({ customText, setCustomText, zoneConfigs, logoImage, setLogoImage, onLogoUpload, textColor, setTextColor, onReset, warningMessage }) => {
  // zoneConfigs is an array of zone objects from customization.json
  const zoneCount = zoneConfigs?.length || 1;
  
  // Use the minimum maxChars from all zones for validation
  const maxChars = zoneConfigs ? Math.min(...zoneConfigs.map(z => z.maxChars || 20)) : 20;
  const charsLeft = maxChars - customText.length;

  const colorOptions = [
    { name: 'Black', value: '#000000', class: 'bg-black' },
    { name: 'White', value: '#FFFFFF', class: 'bg-white border-2 border-gray-300' },
    { name: 'Gold', value: '#ff9100ff', class: 'bg-yellow-500' },
  ];

  const handleLogoUpload = (e) => {
    const file = e.target.files[0];
    if (file) {
      // For preview
      const reader = new FileReader();
      reader.onload = (event) => {
        setLogoImage(event.target.result);
      };
      reader.readAsDataURL(file);
      
      // For backend submission
      if (typeof onLogoUpload === 'function') {
        onLogoUpload(file);
      }
    }
  };

  const handleTextChange = (value) => {
    if (value.length <= maxChars) {
      setCustomText(value);
    }
  };

  return (
    <div className="bg-white p-6 rounded-3xl border border-gray-100 shadow-xl space-y-6">
      {/* Text Color Selection */}
      <div>
        <label className="text-sm font-bold text-gray-700 flex items-center gap-2 mb-3">
          <Palette size={16} className="text-primary" /> Text Color
        </label>
        <div className="flex gap-3">
          {colorOptions.map((color) => (
            <button
              key={color.value}
              onClick={() => setTextColor(color.value)}
              className={`flex-1 py-3 px-4 rounded-xl border-2 font-medium text-sm transition-all flex items-center justify-center gap-2 ${
                textColor === color.value
                  ? 'border-primary bg-primary/5 shadow-md'
                  : 'border-gray-200 hover:border-gray-300 bg-white'
              }`}
            >
              <span className={`w-5 h-5 rounded-full ${color.class} shadow-sm`}></span>
              <span className="text-gray-700">{color.name}</span>
            </button>
          ))}
        </div>
      </div>

      {/* Text Customization - Single Input for All Zones */}
      <div>
        <div className="flex items-center justify-between mb-2">
          <label className="text-sm font-bold text-gray-700 flex items-center gap-2">
            <Type size={16} className="text-primary" /> Personalized Text
          </label>
          <span className={`text-xs font-medium ${charsLeft < 3 ? 'text-red-500' : 'text-gray-400'}`}>
            {charsLeft} chars left
          </span>
        </div>
        
        <div className="relative">
          <input
            type="text"
            value={customText}
            onChange={(e) => handleTextChange(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === 'Enter') {
                e.preventDefault();
              }
            }}
            placeholder="Type your message here..."
            className={`w-full px-4 py-4 bg-gray-50 border-2 ${warningMessage ? 'border-red-500/50 focus:border-red-500 focus:bg-red-50/20' : 'border-transparent focus:border-primary/20 focus:bg-white'} rounded-2xl outline-none transition-all font-medium text-lg placeholder:text-gray-300`}
            autoComplete="off"
            spellCheck="false"
          />
        </div>
        
        {zoneCount > 1 && (
          <p className="text-xs text-gray-500 mt-2 flex items-center gap-1">
            <AlertCircle size={12} /> 
            Text will appear in all {zoneCount} zones on the product
          </p>
        )}
        
        {warningMessage && (
          <p className="text-red-500 text-xs font-bold mt-2 flex items-center gap-1">
            <AlertCircle size={12} /> {warningMessage}
          </p>
        )}
      </div>

      {/* Logo Upload Section */}
      <div>
        <label className="text-sm font-bold text-gray-700 flex items-center gap-2 mb-2">
          <ImageIcon size={16} className="text-primary" /> Corporate Logo
        </label>
        
        {logoImage ? (
          <div className="relative inline-block group">
            <img 
              src={logoImage} 
              alt="Uploaded Logo" 
              className="w-24 h-24 object-contain rounded-xl border border-gray-100 bg-gray-50 p-2"
            />
            <button 
              onClick={() => setLogoImage(null)}
              className="absolute -top-2 -right-2 bg-red-500 text-white rounded-full p-1 shadow-lg opacity-0 group-hover:opacity-100 transition-opacity"
            >
              <X size={14} />
            </button>
          </div>
        ) : (
          <label className="flex flex-col items-center justify-center w-full h-32 border-2 border-dashed border-gray-200 rounded-2xl cursor-pointer hover:bg-gray-50 hover:border-primary/30 transition-all">
            <div className="flex flex-col items-center justify-center pt-5 pb-6 text-gray-400">
              <ImageIcon size={32} className="mb-2" />
              <p className="text-sm font-bold">Upload Company Logo</p>
              <p className="text-xs">PNG, JPG or SVG (Max 2MB)</p>
            </div>
            <input type="file" className="hidden" accept="image/*" onChange={handleLogoUpload} />
          </label>
        )}
      </div>

      <div className="flex flex-col sm:flex-row gap-4">
        <button
          onClick={onReset}
          className="flex-1 px-6 py-4 bg-gray-100 text-gray-500 rounded-2xl flex items-center justify-center hover:bg-gray-200 transition-colors active:scale-95"
          title="Reset Customization"
        >
          <RefreshCcw size={20} />
          <span className="ml-2 sm:hidden font-bold">Reset</span>
        </button>
      </div>

      <div className="flex gap-3 p-4 bg-blue-50/50 rounded-2xl border border-blue-100 text-blue-700 text-xs leading-relaxed">
        <AlertCircle size={14} className="shrink-0 mt-0.5" />
        <p>
          <strong>Note:</strong> This is a real-time preview. Our designers will manually adjust the branding for bulk orders to ensure perfect alignment.
        </p>
      </div>
    </div>
  );
};

export default CustomizerControls;
