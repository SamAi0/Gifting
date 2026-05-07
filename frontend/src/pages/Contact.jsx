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
      <section className="py-6 md:py-10 bg-white border-b border-slate-100 overflow-hidden relative">
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

      <div className="container-custom py-6 md:py-10">
          {/* Contact Information */}
          <div className="lg:col-span-12 space-y-4">
            <div className="text-center max-w-3xl mx-auto">
              <h2 className="text-3xl md:text-4xl font-bold text-slate-900 mb-6">Our Information</h2>
              <p className="text-slate-500 text-lg leading-relaxed font-light mb-10">
                Reach out to us directly or visit our office. Our team is committed to providing premium support for all your corporate requirements.
              </p>
            </div>

            <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
               {[
                 { icon: MapPin, title: 'Registered Office', detail: 'Shop C, Jai Ganesh Society, Sector 3, Airoli, Navi Mumbai - 400708' },
                 { icon: Phone, title: 'Call Center', detail: '+91 81699 75287 / +91 70214 95439' },
                 { icon: Mail, title: 'Email Address', detail: 'corporate@sohamgift.com' },
                 { icon: Clock, title: 'Business Hours', detail: 'Mon - Fri: 10AM - 7PM, Sat: 10AM - 3PM' },
               ].map((item, idx) => (
                 <motion.div 
                   key={idx}
                   initial={{ opacity: 0, y: 20 }}
                   whileInView={{ opacity: 1, y: 0 }}
                   transition={{ delay: idx * 0.1 }}
                   className="flex flex-col items-center text-center p-6 bg-white rounded-3xl border border-slate-100 shadow-premium group hover:border-primary/20 transition-all duration-500"
                 >
                    <div className="w-16 h-16 rounded-2xl bg-slate-50 flex items-center justify-center text-primary shadow-sm group-hover:bg-primary group-hover:text-white transition-all duration-500 mb-6">
                       <item.icon size={28} />
                    </div>
                    <h4 className="text-lg font-bold text-slate-900 mb-2">{item.title}</h4>
                    <p className="text-slate-500 text-sm leading-relaxed font-medium">{item.detail}</p>
                 </motion.div>
               ))}
            </div>

          </div>
        </div>

    </div>
  );
};

export default Contact;

