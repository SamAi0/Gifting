import { Heart, Target, TrendingUp, ShieldCheck, Award, Zap, Users } from 'lucide-react';
import { motion } from 'framer-motion';

const About = () => {
  return (
    <div className="pt-32 bg-slate-50 min-h-screen">
      {/* Hero Section */}
      <section className="py-24 container-custom overflow-hidden relative">
         <div className="absolute top-0 right-0 w-[500px] h-[500px] bg-primary/5 rounded-full blur-[120px] -mr-40 -mt-40"></div>
         
         <div className="grid lg:grid-cols-2 gap-16 items-center">
            <motion.div
              initial={{ opacity: 0, x: -30 }}
              animate={{ opacity: 1, x: 0 }}
            >
               <span className="inline-block py-1.5 px-4 rounded-full bg-primary/10 text-primary text-[10px] font-black uppercase tracking-[0.3em] mb-6">Our Legacy</span>
               <h1 className="text-5xl md:text-7xl font-bold text-slate-900 mb-8 leading-tight tracking-tight">Redefining <span className="text-primary italic">Excellence</span> in Gifting</h1>
               <p className="text-xl text-slate-500 leading-relaxed mb-10 font-light">
                 Since 2019, Soham Gift has been at the forefront of the corporate gifting revolution in India, transforming simple exchanges into powerful brand statements.
               </p>
               <div className="grid grid-cols-2 gap-6">
                  <div className="bg-white p-8 rounded-3xl shadow-premium border border-slate-100">
                    <p className="text-4xl font-black text-slate-900 mb-2 tracking-tighter">500+</p>
                    <p className="text-slate-400 text-xs font-black uppercase tracking-widest">Enterprise Clients</p>
                  </div>
                  <div className="bg-white p-8 rounded-3xl shadow-premium border border-slate-100">
                    <p className="text-4xl font-black text-slate-900 mb-2 tracking-tighter">10k+</p>
                    <p className="text-slate-400 text-xs font-black uppercase tracking-widest">Success Stories</p>
                  </div>
               </div>
            </motion.div>
            <motion.div 
               initial={{ opacity: 0, scale: 0.9 }}
               animate={{ opacity: 1, scale: 1 }}
               className="relative"
            >
               <div className="absolute -inset-4 bg-primary/20 rounded-[3rem] blur-2xl -z-10 animate-pulse"></div>
               <img 
                 src="https://images.unsplash.com/photo-1513201099705-a9746e1e201f?auto=format&fit=crop&q=80&w=1200" 
                 className="rounded-[3rem] shadow-3xl w-full h-[600px] object-cover"
                 alt="Our Story"
               />
               <div className="absolute bottom-10 left-10 glass-card p-8 border-white/50 max-w-[280px]">
                  <Award className="text-primary mb-4" size={32} />
                  <p className="text-slate-900 font-bold leading-snug">Awarded Best Corporate Gifting Partner 2023</p>
               </div>
            </motion.div>
         </div>
      </section>

      {/* Values Section */}
      <section className="bg-slate-900 py-32 relative overflow-hidden">
         <div className="absolute top-0 left-1/2 -translate-x-1/2 w-full h-full bg-[radial-gradient(circle_at_center,rgba(217,22,86,0.1),transparent_70%)]"></div>
         
         <div className="container-custom relative z-10">
            <div className="text-center mb-24">
               <span className="text-primary font-black uppercase tracking-[0.3em] text-xs mb-4 inline-block">The DNA of Our Service</span>
               <h2 className="text-4xl md:text-6xl font-bold text-white tracking-tight">Our Core <span className="text-primary italic">Values</span></h2>
            </div>
            
            <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
               {[
                 { icon: Heart, title: 'Client Centricity', desc: 'We don\'t just deliver products; we build long-term relationships through empathy.' },
                 { icon: ShieldCheck, title: 'Absolute Quality', desc: 'Rigorous 3-step quality assurance before any gift leaves our warehouse.' },
                 { icon: Zap, title: 'Rapid Execution', desc: 'Deadlines are sacred. We ensure your appreciation arrives precisely on time.' },
                 { icon: Users, title: 'Social Impact', desc: 'We source responsibly and support local artisans in our premium collections.' }
               ].map((item, idx) => (
                 <motion.div 
                   key={idx}
                   initial={{ opacity: 0, y: 20 }}
                   whileInView={{ opacity: 1, y: 0 }}
                   viewport={{ once: true }}
                   transition={{ delay: idx * 0.1 }}
                   className="p-10 bg-white/5 rounded-[2.5rem] border border-white/10 hover:bg-white/10 transition-all duration-500 group"
                 >
                    <div className="w-16 h-16 bg-primary/20 text-primary rounded-2xl flex items-center justify-center mb-8 group-hover:scale-110 group-hover:bg-primary group-hover:text-white transition-all duration-500">
                       <item.icon size={28} />
                    </div>
                    <h4 className="text-xl font-bold text-white mb-4">{item.title}</h4>
                    <p className="text-slate-400 text-sm leading-relaxed font-light">{item.desc}</p>
                 </motion.div>
               ))}
            </div>
         </div>
      </section>

      {/* Mission Vision */}
      <section className="py-32 container-custom">
         <div className="grid md:grid-cols-2 gap-10">
            <motion.div 
               whileHover={{ y: -10 }}
               className="bg-white p-16 rounded-[3rem] shadow-premium border border-slate-100 flex flex-col items-center text-center group transition-all duration-500"
            >
               <div className="w-24 h-24 bg-slate-50 rounded-3xl shadow-sm flex items-center justify-center mb-10 text-primary group-hover:bg-primary group-hover:text-white transition-all duration-500">
                  <Target size={40} />
               </div>
               <h3 className="text-3xl font-bold text-slate-900 mb-6 tracking-tight">Our Mission</h3>
               <p className="text-slate-500 text-lg font-light leading-relaxed">
                 To empower businesses with a world-class gifting ecosystem that combines human emotion with technological precision, making appreciation effortless.
               </p>
            </motion.div>
            
            <motion.div 
               whileHover={{ y: -10 }}
               className="bg-white p-16 rounded-[3rem] shadow-premium border border-slate-100 flex flex-col items-center text-center group transition-all duration-500"
            >
               <div className="w-24 h-24 bg-slate-50 rounded-3xl shadow-sm flex items-center justify-center mb-10 text-primary group-hover:bg-primary group-hover:text-white transition-all duration-500">
                  <TrendingUp size={40} />
               </div>
               <h3 className="text-3xl font-bold text-slate-900 mb-6 tracking-tight">Our Vision</h3>
               <p className="text-slate-500 text-lg font-light leading-relaxed">
                 To be the global benchmark for corporate gifting, where every brand, regardless of size, can express gratitude through curated, sustainable, and impactful gifts.
               </p>
            </motion.div>
         </div>
      </section>

      {/* CTA Section */}
      <section className="pb-32 container-custom">
         <div className="bg-primary p-16 md:p-24 rounded-[4rem] text-white text-center relative overflow-hidden shadow-3xl">
            <div className="absolute inset-0 bg-[url('https://www.transparenttextures.com/patterns/carbon-fibre.png')] opacity-10"></div>
            <div className="relative z-10">
               <h2 className="text-4xl md:text-6xl font-bold mb-8 tracking-tight">Ready to start your <br /><span className="italic">gifting journey?</span></h2>
               <div className="flex flex-col sm:flex-row gap-6 justify-center">
                  <button className="bg-white text-primary px-10 py-5 rounded-2xl font-bold text-lg hover:bg-slate-900 hover:text-white transition-all duration-300">View Our Collections</button>
                  <button className="bg-slate-900/20 backdrop-blur-md border border-white/20 px-10 py-5 rounded-2xl font-bold text-lg hover:bg-slate-900 transition-all duration-300">Talk to an Expert</button>
               </div>
            </div>
         </div>
      </section>
    </div>
  );
};

export default About;

