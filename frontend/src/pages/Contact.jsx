import { useState } from 'react';
import { MapPin, Phone, Mail, Clock, Send, CheckCircle, ArrowRight, ShieldCheck, ArrowUpRight } from 'lucide-react';
import { submitContact } from '../api';
import { motion, AnimatePresence } from 'framer-motion';

const Contact = () => {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    phone: '',
    message: '',
  });
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [isSuccess, setIsSuccess] = useState(false);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsSubmitting(true);
    try {
      await submitContact(formData);
      setIsSuccess(true);
      setFormData({ name: '', email: '', phone: '', message: '' });
    } catch (error) {
      console.error("Error submitting contact form:", error);
      alert("Something went wrong. Please try again.");
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="pt-32 bg-slate-50 min-h-screen">
      {/* Header Section */}
      <section className="py-24 bg-white border-b border-slate-100 overflow-hidden relative">
         {/* Decorative Glow */}
         <div className="absolute top-0 right-0 w-96 h-96 bg-primary/5 rounded-full blur-[100px] -mr-20 -mt-20"></div>
         <div className="absolute bottom-0 left-0 w-64 h-64 bg-blue-500/5 rounded-full blur-[80px] -ml-20 -mb-20"></div>

         <div className="container-custom relative z-10 text-center">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
            >
              <span className="inline-block py-1.5 px-4 rounded-full bg-primary/10 text-primary text-[10px] font-black uppercase tracking-[0.3em] mb-6">Connect with Us</span>
              <h1 className="text-5xl md:text-7xl font-bold text-slate-900 mb-8 tracking-tight">Let's Discuss Your <span className="text-primary italic">Gifting</span> Goals</h1>
              <p className="text-xl text-slate-500 max-w-2xl mx-auto font-light leading-relaxed">
                Whether it's a small team appreciation or a global corporate event, our experts are ready to craft the perfect strategy for you.
              </p>
            </motion.div>
         </div>
      </section>

      <div className="container-custom py-24">
        <div className="grid lg:grid-cols-12 gap-16 items-start">
          {/* Contact Information */}
          <div className="lg:col-span-5 space-y-12">
            <div>
              <h2 className="text-3xl font-bold text-slate-900 mb-6">Our Information</h2>
              <p className="text-slate-500 text-lg leading-relaxed font-light mb-10">
                Reach out to us directly or visit our office. Our team is committed to providing premium support for all your corporate requirements.
              </p>
            </div>

            <div className="space-y-8">
               {[
                 { icon: MapPin, title: 'Registered Office', detail: 'Shop C, Jai Ganesh Society, Sector 3, Airoli, Navi Mumbai - 400708', color: 'primary' },
                 { icon: Phone, title: 'Call Center', detail: '+91 81699 75287 / +91 70214 95439', color: 'slate-900' },
                 { icon: Mail, title: 'Email Address', detail: 'corporate@sohamgift.com', color: 'slate-900' },
                 { icon: Clock, title: 'Business Hours', detail: 'Mon - Fri: 10AM - 7PM, Sat: 10AM - 3PM', color: 'green-600' },
               ].map((item, idx) => (
                 <motion.div 
                   key={idx}
                   initial={{ opacity: 0, x: -20 }}
                   whileInView={{ opacity: 1, x: 0 }}
                   transition={{ delay: idx * 0.1 }}
                   className="flex gap-6 group"
                 >
                    <div className={`w-14 h-14 rounded-2xl bg-white border border-slate-200 flex items-center justify-center text-primary shadow-sm group-hover:bg-primary group-hover:text-white transition-all duration-500`}>
                       <item.icon size={24} />
                    </div>
                    <div>
                      <h4 className="text-lg font-bold text-slate-900 mb-1">{item.title}</h4>
                      <p className="text-slate-500 text-sm leading-relaxed font-medium">{item.detail}</p>
                    </div>
                 </motion.div>
               ))}
            </div>

            <div className="p-8 rounded-3xl bg-slate-900 text-white relative overflow-hidden shadow-2xl">
               <div className="relative z-10">
                  <h4 className="text-xl font-bold mb-4">Fast Response Guarantee</h4>
                  <p className="text-slate-400 text-sm leading-relaxed mb-6">
                    Our dedicated account managers typically respond to all inquiries within <span className="text-white font-bold italic">2 business hours</span>.
                  </p>
                  <div className="flex items-center gap-2 text-primary font-bold text-sm">
                    <ShieldCheck size={18} /> Verified Corporate Partner
                  </div>
               </div>
               <div className="absolute top-0 right-0 w-32 h-32 bg-primary/20 rounded-full blur-3xl"></div>
            </div>
          </div>

          {/* Contact Form */}
          <div className="lg:col-span-7">
            <motion.div 
               initial={{ opacity: 0, scale: 0.95 }}
               animate={{ opacity: 1, scale: 1 }}
               className="bg-white rounded-[3rem] p-8 md:p-12 shadow-premium border border-slate-100"
            >
               <AnimatePresence mode="wait">
                  {isSuccess ? (
                     <motion.div 
                        key="success"
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        className="text-center py-20"
                     >
                        <div className="w-24 h-24 bg-green-100 text-green-600 rounded-full flex items-center justify-center mx-auto mb-8">
                           <CheckCircle size={48} />
                        </div>
                        <h3 className="text-4xl font-bold text-slate-900 mb-4">Message Received</h3>
                        <p className="text-slate-500 text-lg mb-12 max-w-sm mx-auto font-light">Your inquiry has been sent to our corporate team. We'll be in touch very shortly.</p>
                        <button 
                           onClick={() => setIsSuccess(false)} 
                           className="text-primary font-bold hover:underline flex items-center gap-2 mx-auto"
                        >
                           Send another message <ArrowRight size={18} />
                        </button>
                     </motion.div>
                  ) : (
                     <form onSubmit={handleSubmit} className="space-y-8">
                        <div className="mb-10">
                           <h3 className="text-2xl font-bold text-slate-900 mb-2">Send us a Message</h3>
                           <p className="text-slate-400 font-light text-sm">Fill out the form below and we'll get back to you.</p>
                        </div>

                        <div className="space-y-6">
                           <div className="space-y-2 group">
                              <label className="text-[10px] font-black text-slate-400 uppercase tracking-widest ml-4 group-focus-within:text-primary transition-colors">Full Name</label>
                              <input 
                                required
                                type="text" 
                                name="name"
                                className="w-full px-6 py-5 rounded-2xl bg-slate-50 border border-slate-100 focus:bg-white focus:ring-4 focus:ring-primary/5 focus:border-primary focus:outline-none transition-all text-slate-700 font-medium"
                                value={formData.name}
                                onChange={handleInputChange}
                                placeholder="e.g. Rahul Sharma"
                              />
                           </div>

                           <div className="grid md:grid-cols-2 gap-8">
                              <div className="space-y-2 group">
                                 <label className="text-[10px] font-black text-slate-400 uppercase tracking-widest ml-4 group-focus-within:text-primary transition-colors">Business Email</label>
                                 <input 
                                   required
                                   type="email" 
                                   name="email"
                                   className="w-full px-6 py-5 rounded-2xl bg-slate-50 border border-slate-100 focus:bg-white focus:ring-4 focus:ring-primary/5 focus:border-primary focus:outline-none transition-all text-slate-700 font-medium"
                                   value={formData.email}
                                   onChange={handleInputChange}
                                   placeholder="rahul@company.com"
                                 />
                              </div>
                              <div className="space-y-2 group">
                                 <label className="text-[10px] font-black text-slate-400 uppercase tracking-widest ml-4 group-focus-within:text-primary transition-colors">Phone Number</label>
                                 <input 
                                   required
                                   type="tel" 
                                   name="phone"
                                   className="w-full px-6 py-5 rounded-2xl bg-slate-50 border border-slate-100 focus:bg-white focus:ring-4 focus:ring-primary/5 focus:border-primary focus:outline-none transition-all text-slate-700 font-medium"
                                   value={formData.phone}
                                   onChange={handleInputChange}
                                   placeholder="+91 98765 43210"
                                 />
                              </div>
                           </div>

                           <div className="space-y-2 group">
                              <label className="text-[10px] font-black text-slate-400 uppercase tracking-widest ml-4 group-focus-within:text-primary transition-colors">Your Inquiry</label>
                              <textarea 
                                required
                                name="message"
                                rows="5"
                                className="w-full px-6 py-5 rounded-2xl bg-slate-50 border border-slate-100 focus:bg-white focus:ring-4 focus:ring-primary/5 focus:border-primary focus:outline-none transition-all text-slate-700 font-medium resize-none"
                                value={formData.message}
                                onChange={handleInputChange}
                                placeholder="Tell us about your requirements (quantity, occasion, etc.)"
                              ></textarea>
                           </div>
                        </div>

                        <button 
                          type="submit" 
                          disabled={isSubmitting}
                          className="btn-primary w-full py-6 text-xl shadow-2xl shadow-primary/30"
                        >
                          {isSubmitting ? (
                            <span className="flex items-center gap-3">
                               <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin"></div>
                               Processing...
                            </span>
                          ) : (
                            <span className="flex items-center gap-3">
                               Confirm Submission <Send size={20} />
                            </span>
                          )}
                        </button>
                     </form>
                  )}
               </AnimatePresence>
            </motion.div>
          </div>
        </div>
      </div>

      {/* Map Section */}
      <section className="section-padding bg-white">
         <div className="container-custom">
            <div className="relative rounded-[3rem] overflow-hidden shadow-3xl h-[500px] border border-slate-100">
               {/* In a real app, I'd use an iframe or map component here. Using a premium visual placeholder */}
               <div className="absolute inset-0 bg-slate-100 flex items-center justify-center">
                  <div className="text-center">
                     <MapPin className="text-primary mx-auto mb-4 animate-bounce" size={48} />
                     <p className="text-slate-400 font-bold uppercase tracking-widest text-sm">Interactive Map Location</p>
                  </div>
               </div>
               <img src="https://images.unsplash.com/photo-1524661135-423995f22d0b?auto=format&fit=crop&q=80&w=2000" className="w-full h-full object-cover opacity-20 grayscale" alt="Map Area" />
               <div className="absolute bottom-10 left-10 glass-card p-8 border-slate-200/50 max-w-sm">
                  <h4 className="text-xl font-bold text-slate-900 mb-2">Soham Gift HQ</h4>
                  <p className="text-slate-500 text-sm leading-relaxed mb-4">Airoli Sector 3, Navi Mumbai, Maharashtra. Near the Airoli Railway Station for easy accessibility.</p>
                  <button className="text-primary font-bold text-sm flex items-center gap-2 group">
                     Open in Google Maps <ArrowUpRight size={16} className="group-hover:translate-x-1 group-hover:-translate-y-1 transition-transform" />
                  </button>
               </div>
            </div>
         </div>
      </section>
    </div>
  );
};

export default Contact;

