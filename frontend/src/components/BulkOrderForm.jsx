import { useState } from 'react';
import { Building2, Mail, Phone, Users, Package, ArrowRight, MessageCircle } from 'lucide-react';
import { submitBulkOrder } from '../api';

const BulkOrderForm = () => {
  const [formData, setFormData] = useState({
    fullName: '',
    email: '',
    phone: '',
    companyName: '',
    employeeCount: '0-10',
    lookingFor: 'Joining Kits',
    customMessage: ''
  });
  const [status, setStatus] = useState('idle'); // 'idle', 'submitting', 'success', 'error'

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setStatus('submitting');
    
    try {
      const payload = {
        company_name: formData.companyName,
        contact_person: formData.fullName,
        email: formData.email,
        phone: formData.phone,
        message: `Employee Count: ${formData.employeeCount}\nLooking For: ${formData.lookingFor}\nCustom Message: ${formData.customMessage}`
      };
      
      await submitBulkOrder(payload);
      setStatus('success');
      setFormData({
        fullName: '',
        email: '',
        phone: '',
        companyName: '',
        employeeCount: '0-10',
        lookingFor: 'Joining Kits',
        customMessage: ''
      });
    } catch (error) {
      console.error('Failed to submit bulk order:', error);
      setStatus('error');
    }
  };

  const handleWhatsApp = () => {
    const message = `Hi, I am interested in Bulk Corporate Gifting.\n\n*Name:* ${formData.fullName}\n*Company:* ${formData.companyName}\n*Contact Number:* ${formData.phone}\n*Business Email:* ${formData.email}\n*Employee Count:* ${formData.employeeCount}\n*Looking for:* ${formData.lookingFor}\n*Custom Requirements:* ${formData.customMessage}\n\nPlease share more details.`;
    const whatsappUrl = `https://wa.me/918657631208?text=${encodeURIComponent(message)}`;
    window.open(whatsappUrl, '_blank');
  };

  return (
    <section className="py-12 md:py-20 bg-slate-50 relative overflow-hidden" id="bulk-order">
      {/* Abstract Background */}
      <div className="absolute top-0 right-0 w-1/3 h-full z-0 opacity-10 pointer-events-none">
        <div className="absolute top-1/4 right-0 w-64 h-64 bg-primary rounded-full blur-[100px]"></div>
      </div>

      <div className="container-home relative z-10">
        <div className="grid lg:grid-cols-2 gap-12 lg:gap-20 items-center">
          
          {/* Left Text Side */}
          <div className="text-left">
            <span className="inline-block py-1.5 px-4 bg-primary/10 text-primary rounded-full text-[10px] font-black uppercase tracking-widest mb-4">
              Bulk Orders
            </span>
            <h2 className="text-4xl md:text-5xl font-bold text-slate-900 mb-6 leading-tight">
              Solutions For Your Business, <br/>
              <span className="text-primary italic font-serif">One at a Time.</span>
            </h2>
            <p className="text-lg text-slate-500 leading-relaxed mb-8 font-light">
              We understand the unique needs of each industry, and that's why we're the go-to partner for Event Planners, Illustrators, Corporates, Restaurant Chains, Retail Stores & Consumer Brands alike!
            </p>
            
            <div className="grid grid-cols-2 gap-6 mb-8">
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 rounded-full bg-white shadow-sm flex items-center justify-center text-primary">
                  <Building2 size={18} />
                </div>
                <span className="text-sm font-bold text-slate-700">Corporates</span>
              </div>
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 rounded-full bg-white shadow-sm flex items-center justify-center text-primary">
                  <Users size={18} />
                </div>
                <span className="text-sm font-bold text-slate-700">Event Planners</span>
              </div>
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 rounded-full bg-white shadow-sm flex items-center justify-center text-primary">
                  <Package size={18} />
                </div>
                <span className="text-sm font-bold text-slate-700">Retail Stores</span>
              </div>
            </div>
          </div>

          {/* Right Form Side */}
          <div className="bg-white rounded-[2rem] p-6 md:p-8 shadow-premium border border-slate-100">
            <h3 className="text-2xl font-bold text-slate-900 mb-2">Bulk Orders Tailored to Your Needs</h3>
            <p className="text-slate-500 text-sm mb-6">Fill the Form Today!</p>

            {status === 'success' ? (
              <div className="bg-green-50 text-green-700 p-6 rounded-2xl border border-green-100 text-center">
                <div className="w-12 h-12 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-3">
                  <span className="text-2xl">✓</span>
                </div>
                <h4 className="font-bold text-lg mb-1">Thank You!</h4>
                <p className="text-sm">We have received your order request. Our corporate team will contact you shortly.</p>
                <button onClick={() => setStatus('idle')} className="mt-4 text-green-700 font-bold text-sm underline">Submit another</button>
              </div>
            ) : (
              <form onSubmit={handleSubmit} className="space-y-4">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div className="space-y-1.5">
                    <label className="text-[10px] font-black text-slate-400 uppercase tracking-widest">Full Name *</label>
                    <input required type="text" name="fullName" value={formData.fullName} onChange={handleChange} className="w-full px-4 py-3 bg-slate-50 border border-slate-100 rounded-xl focus:border-primary/50 focus:bg-white outline-none transition-all text-sm" placeholder="e.g. Sakshi Jain" />
                  </div>
                  <div className="space-y-1.5">
                    <label className="text-[10px] font-black text-slate-400 uppercase tracking-widest">Business Email *</label>
                    <input required type="email" name="email" value={formData.email} onChange={handleChange} className="w-full px-4 py-3 bg-slate-50 border border-slate-100 rounded-xl focus:border-primary/50 focus:bg-white outline-none transition-all text-sm" placeholder="sakshi@company.com" />
                  </div>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div className="space-y-1.5">
                    <label className="text-[10px] font-black text-slate-400 uppercase tracking-widest">Contact Number *</label>
                    <input required type="tel" name="phone" value={formData.phone} onChange={handleChange} className="w-full px-4 py-3 bg-slate-50 border border-slate-100 rounded-xl focus:border-primary/50 focus:bg-white outline-none transition-all text-sm" placeholder="9899899989" />
                  </div>
                  <div className="space-y-1.5">
                    <label className="text-[10px] font-black text-slate-400 uppercase tracking-widest">Company Name *</label>
                    <input required type="text" name="companyName" value={formData.companyName} onChange={handleChange} className="w-full px-4 py-3 bg-slate-50 border border-slate-100 rounded-xl focus:border-primary/50 focus:bg-white outline-none transition-all text-sm" placeholder="e.g. Carteasy Pvt Ltd" />
                  </div>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div className="space-y-1.5">
                    <label className="text-[10px] font-black text-slate-400 uppercase tracking-widest">Employee Count</label>
                    <select name="employeeCount" value={formData.employeeCount} onChange={handleChange} className="w-full px-4 py-3 bg-slate-50 border border-slate-100 rounded-xl focus:border-primary/50 focus:bg-white outline-none transition-all text-sm">
                      <option value="0-10">0-10</option>
                      <option value="11-50">11-50</option>
                      <option value="51-200">51-200</option>
                      <option value="200+">200+</option>
                    </select>
                  </div>
                  <div className="space-y-1.5">
                    <label className="text-[10px] font-black text-slate-400 uppercase tracking-widest">What are you looking for?</label>
                    <select name="lookingFor" value={formData.lookingFor} onChange={handleChange} className="w-full px-4 py-3 bg-slate-50 border border-slate-100 rounded-xl focus:border-primary/50 focus:bg-white outline-none transition-all text-sm">
                      <option value="Joining Kits">Joining Kits</option>
                      <option value="Festival Gifts">Festival Gifts</option>
                      <option value="Custom Merchandise">Custom Merchandise</option>
                      <option value="Employee Rewards">Employee Rewards</option>
                      <option value="Other">Other</option>
                    </select>
                  </div>
                </div>

                <div className="space-y-1.5">
                  <label className="text-[10px] font-black text-slate-400 uppercase tracking-widest">Custom Requirements / Message</label>
                  <textarea name="customMessage" value={formData.customMessage} onChange={handleChange} rows="3" className="w-full px-4 py-3 bg-slate-50 border border-slate-100 rounded-xl focus:border-primary/50 focus:bg-white outline-none transition-all text-sm" placeholder="Any specific customization requests or brand colors?"></textarea>
                </div>

                {status === 'error' && (
                  <p className="text-red-500 text-xs font-bold">Failed to submit order request. Please try again or use WhatsApp.</p>
                )}

                <div className="pt-2 flex flex-col sm:flex-row gap-3">
                  <button 
                    type="submit" 
                    disabled={status === 'submitting'}
                    className="flex-1 btn-primary py-4 rounded-xl flex items-center justify-center gap-2 font-bold shadow-lg shadow-primary/20"
                  >
                    {status === 'submitting' ? 'Submitting...' : 'Get Quote'} <ArrowRight size={16} />
                  </button>
                  <button 
                    type="button"
                    onClick={handleWhatsApp}
                    className="flex-1 py-4 bg-[#25D366] hover:bg-[#128C7E] text-white rounded-xl flex items-center justify-center gap-2 font-bold shadow-lg shadow-[#25D366]/20 transition-all"
                  >
                    <MessageCircle size={18} /> WhatsApp Us
                  </button>
                </div>
              </form>
            )}
          </div>
        </div>
      </div>
    </section>
  );
};

export default BulkOrderForm;
