import { Heart, Target, TrendingUp, ShieldCheck, Award, Zap, Users } from 'lucide-react';
import { motion } from 'framer-motion';

const About = () => {
  return (
    <div className="pt-32 bg-slate-50 min-h-screen">
      {/* Hero Section */}
      <section className="py-10 md:py-16 container-custom overflow-hidden relative">
         <div className="absolute top-0 right-0 w-[500px] h-[500px] bg-primary/5 rounded-full blur-[120px] -mr-40 -mt-40"></div>
         
         <div className="grid lg:grid-cols-2 gap-10 items-center">
            <motion.div
              initial={{ opacity: 0, x: -30 }}
              animate={{ opacity: 1, x: 0 }}
            >
               <span className="inline-block py-1 px-3 rounded-full bg-primary/10 text-primary text-[10px] font-black uppercase tracking-[0.3em] mb-4">Our Legacy</span>
               <h1 className="text-4xl md:text-5xl font-bold text-slate-900 mb-6 leading-tight tracking-tight">Redefining <span className="text-primary italic">Excellence</span> in Gifting</h1>
               <p className="text-lg text-slate-500 leading-relaxed mb-8 font-light">
                 Since 2019, Soham Gift has been at the forefront of the corporate gifting revolution in India, transforming simple exchanges into powerful brand statements.
               </p>
               <div className="grid grid-cols-2 gap-4">
                  <div className="bg-white p-6 rounded-2xl shadow-premium border border-slate-100">
                    <p className="text-3xl font-black text-slate-900 mb-1 tracking-tighter">500+</p>
                    <p className="text-slate-400 text-[10px] font-black uppercase tracking-widest">Enterprise Clients</p>
                  </div>
                  <div className="bg-white p-6 rounded-2xl shadow-premium border border-slate-100">
                    <p className="text-3xl font-black text-slate-900 mb-1 tracking-tighter">10k+</p>
                    <p className="text-slate-400 text-[10px] font-black uppercase tracking-widest">Success Stories</p>
                  </div>
               </div>
            </motion.div>
            <motion.div 
               initial={{ opacity: 0, scale: 0.9 }}
               animate={{ opacity: 1, scale: 1 }}
               className="relative"
            >
               <div className="absolute -inset-4 bg-primary/20 rounded-[2.5rem] blur-2xl -z-10 animate-pulse"></div>
               <img 
                 src="https://images.unsplash.com/photo-1513201099705-a9746e1e201f?auto=format&fit=crop&q=80&w=1200" 
                 className="rounded-[2.5rem] shadow-3xl w-full h-[450px] object-cover"
                 alt="Our Story"
               />
               <div className="absolute bottom-6 left-6 glass-card p-6 border-white/50 max-w-[240px]">
                  <Award className="text-primary mb-2" size={24} />
                  <p className="text-slate-900 font-bold leading-snug text-sm">Awarded Best Corporate Gifting Partner 2023</p>
               </div>
            </motion.div>
         </div>
      </section>

      {/* Values Section */}
      <section className="bg-slate-900 py-12 md:py-20 relative overflow-hidden">
         <div className="absolute top-0 left-1/2 -translate-x-1/2 w-full h-full bg-[radial-gradient(circle_at_center,rgba(217,22,86,0.1),transparent_70%)]"></div>
         
         <div className="container-custom relative z-10">
            <div className="text-center mb-12">
               <span className="text-primary font-black uppercase tracking-[0.3em] text-[10px] mb-3 inline-block">The DNA of Our Service</span>
               <h2 className="text-3xl md:text-5xl font-bold text-white tracking-tight">Our Core <span className="text-primary italic">Values</span></h2>
            </div>
            
            <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
               {[
                 { icon: Heart, title: 'Client Centricity', desc: 'We build long-term relationships through empathy.' },
                 { icon: ShieldCheck, title: 'Absolute Quality', desc: 'Rigorous 3-step quality assurance.' },
                 { icon: Zap, title: 'Rapid Execution', desc: 'Ensuring your appreciation arrives precisely on time.' },
                 { icon: Users, title: 'Social Impact', desc: 'Support local artisans in our premium collections.' }
               ].map((item, idx) => (
                 <motion.div 
                   key={idx}
                   initial={{ opacity: 0, y: 20 }}
                   whileInView={{ opacity: 1, y: 0 }}
                   viewport={{ once: true }}
                   transition={{ delay: idx * 0.1 }}
                   className="p-6 bg-white/5 rounded-[2rem] border border-white/10 hover:bg-white/10 transition-all duration-500 group"
                 >
                    <div className="w-12 h-12 bg-primary/20 text-primary rounded-xl flex items-center justify-center mb-6 group-hover:scale-110 group-hover:bg-primary group-hover:text-white transition-all duration-500">
                       <item.icon size={22} />
                    </div>
                    <h4 className="text-lg font-bold text-white mb-2">{item.title}</h4>
                    <p className="text-slate-400 text-xs leading-relaxed font-light">{item.desc}</p>
                 </motion.div>
               ))}
            </div>
         </div>
      </section>

      {/* Mission Vision */}
      <section className="py-12 md:py-20 container-custom">
         <div className="grid md:grid-cols-2 gap-8">
            <motion.div 
               whileHover={{ y: -5 }}
               className="bg-white p-10 rounded-[2.5rem] shadow-premium border border-slate-100 flex flex-col items-center text-center group transition-all duration-500"
            >
               <div className="w-16 h-16 bg-slate-50 rounded-2xl shadow-sm flex items-center justify-center mb-6 text-primary group-hover:bg-primary group-hover:text-white transition-all duration-500">
                  <Target size={32} />
               </div>
               <h3 className="text-2xl font-bold text-slate-900 mb-4 tracking-tight">Our Mission</h3>
               <p className="text-slate-500 text-base font-light leading-relaxed">
                 To empower businesses with a world-class gifting ecosystem that combines human emotion with technological precision.
               </p>
            </motion.div>
            
            <motion.div 
               whileHover={{ y: -5 }}
               className="bg-white p-10 rounded-[2.5rem] shadow-premium border border-slate-100 flex flex-col items-center text-center group transition-all duration-500"
            >
               <div className="w-16 h-16 bg-slate-50 rounded-2xl shadow-sm flex items-center justify-center mb-6 text-primary group-hover:bg-primary group-hover:text-white transition-all duration-500">
                  <TrendingUp size={32} />
               </div>
               <h3 className="text-2xl font-bold text-slate-900 mb-4 tracking-tight">Our Vision</h3>
               <p className="text-slate-500 text-base font-light leading-relaxed">
                 To be the global benchmark for corporate gifting, expressing gratitude through curated, impactful gifts.
               </p>
            </motion.div>
         </div>
      </section>

      {/* CTA Section */}
      <section className="pb-16 container-custom">
         <div className="bg-primary p-10 md:p-16 rounded-[3rem] text-white text-center relative overflow-hidden shadow-3xl">
            <div className="absolute inset-0 bg-[url('https://www.transparenttextures.com/patterns/carbon-fibre.png')] opacity-10"></div>
            <div className="relative z-10">
               <h2 className="text-3xl md:text-5xl font-bold mb-6 tracking-tight">Ready to start your <br /><span className="italic font-serif">gifting journey?</span></h2>
               <div className="flex flex-col sm:flex-row gap-4 justify-center">
                  <button className="bg-white text-primary px-8 py-4 rounded-xl font-bold text-base hover:bg-slate-900 hover:text-white transition-all duration-300">View Collections</button>
                  <button className="bg-slate-900/20 backdrop-blur-md border border-white/20 px-8 py-4 rounded-xl font-bold text-base hover:bg-slate-900 transition-all duration-300">Talk to an Expert</button>
               </div>
            </div>
         </div>
      </section>
    </div>
  );
};

export default About;

