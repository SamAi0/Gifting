import { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { Gift, ShieldCheck, Truck, Clock, ArrowRight, Star, ChevronRight, CheckCircle2, User } from 'lucide-react';
import { fetchProducts, fetchTestimonials, getImageUrl } from '../api';
import { motion } from 'framer-motion';
import { Helmet } from 'react-helmet-async';

const Home = () => {
  const [trendingProducts, setTrendingProducts] = useState([]);
  const [testimonials, setTestimonials] = useState([]);

  useEffect(() => {
    const loadData = async () => {
      try {
        const [prodRes, testimRes] = await Promise.all([
          fetchProducts({ page_size: 24 }), // Fetch enough products for variety
          fetchTestimonials()
        ]);
        const products = prodRes.data.results || prodRes.data;
        // Randomly shuffle products to show a diverse selection
        const shuffled = [...products].sort(() => 0.5 - Math.random());
        setTrendingProducts(shuffled.slice(0, 12));
        const testimonialsData = testimRes.data.results || testimRes.data;
        setTestimonials(testimonialsData.slice(0, 3));
      } catch (error) {
        console.error("Error loading home data:", error);
      }
    };
    loadData();
  }, []);

  return (
    <div className="overflow-hidden bg-white">
      <Helmet>
        <title>Soham Gift | Premium Corporate Gifting Solutions India</title>
        <meta name="description" content="Discover premium corporate gifts for employees, clients, and partners. Customizable bulk gifting solutions with exclusive delivery in Maharashtra." />
      </Helmet>

      {/* Hero Section */}
      <section className="relative min-h-[60vh] flex items-center bg-secondary overflow-hidden">
        {/* Abstract Background Elements */}
        <div className="absolute top-0 right-0 w-1/2 h-full z-0 opacity-20 hidden lg:block">
          <div className="absolute top-1/4 right-1/4 w-96 h-96 bg-primary rounded-full blur-[120px] animate-pulse"></div>
          <div className="absolute bottom-1/4 right-0 w-64 h-64 bg-blue-500 rounded-full blur-[100px]"></div>
        </div>

        <div className="absolute inset-0 z-0">
          <div className="absolute inset-0 bg-gradient-to-r from-secondary via-secondary/95 to-secondary/40 z-10"></div>
          <img
            src="https://images.unsplash.com/photo-1513201099705-a9746e1e201f?auto=format&fit=crop&q=80&w=2000"
            className="w-full h-full object-cover"
            alt="Premium Corporate Gifting"
          />
        </div>

        <div className="relative z-20 w-full px-6 md:px-16 lg:px-24 py-12">
          <div className="max-w-4xl text-left">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6 }}
            >
              <span className="inline-flex items-center gap-2 py-2 px-4 rounded-full bg-white/10 backdrop-blur-md text-primary-light border border-white/10 text-xs font-bold uppercase tracking-widest mb-8">
                <Star size={14} className="fill-primary-light" /> #1 Corporate Gifting Partner
              </span>
              <h1 className="text-5xl md:text-8xl font-bold text-white mb-8 leading-[1.1] tracking-tight">
                Crafting <span className="text-primary italic font-serif">Unforgettable</span> Corporate Moments
              </h1>
              <p className="text-xl text-slate-300 mb-10 max-w-xl leading-relaxed font-light">
                Premium, customizable gifting solutions that transform professional relationships into lasting partnerships.
              </p>
              <div className="flex flex-col sm:flex-row gap-5">
                <Link to="/products" className="btn-primary py-5 px-10 text-lg group">
                  Explore Collections <ChevronRight size={20} className="transition-transform group-hover:translate-x-1" />
                </Link>
                <Link to="/contact" className="btn-outline border-white/20 text-white hover:bg-white hover:text-secondary py-5 px-10 text-lg">
                  Get a Free Consultation
                </Link>
              </div>
            </motion.div>
          </div>
        </div>
      </section>

      {/* Featured Stats */}
      <section className="relative z-30 -mt-12 mb-6">
        <div className="container-custom">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 md:gap-8">
            {[
              { label: 'Happy Clients', value: '500+', icon: User },
              { label: 'Gifts Delivered', value: '25k+', icon: Gift },
              { label: 'Success Rate', value: '99.9%', icon: CheckCircle2 },
              { label: 'Custom Designs', value: '1000+', icon: ShieldCheck },
            ].map((stat, idx) => (
              <motion.div
                key={idx}
                whileHover={{ y: -5 }}
                className="glass-card p-8 text-center flex flex-col items-center justify-center border-t-4 border-t-primary"
              >
                <div className="w-12 h-12 rounded-2xl bg-primary/5 flex items-center justify-center text-primary mb-4">
                  <stat.icon size={24} />
                </div>
                <h4 className="text-3xl font-bold text-slate-900 mb-1">{stat.value}</h4>
                <p className="text-slate-500 text-sm font-medium">{stat.label}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Trending Products */}
      <section className="py-6 md:py-8 bg-slate-50/50 bg-pattern">
        <div className="container-custom">
          <div className="flex flex-col md:flex-row justify-between items-center mb-6 gap-6">
            <div className="text-center md:text-left">
              <h2 className="text-4xl md:text-5xl font-bold mb-4 text-slate-900">Trending Collections</h2>
              <p className="text-slate-500 text-lg max-w-xl">Curated excellence for modern professionals. Explore our most popular corporate gifts.</p>
            </div>
            <Link to="/products" className="btn-secondary group">
              View All Collections <ArrowRight size={18} className="transition-transform group-hover:translate-x-1" />
            </Link>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-8">
            {trendingProducts.length > 0 ? (
              trendingProducts.map((product, idx) => (
                <motion.div
                  key={product.id}
                  initial={{ opacity: 0, y: 20 }}
                  whileInView={{ opacity: 1, y: 0 }}
                  transition={{ delay: idx * 0.1 }}
                  viewport={{ once: true }}
                  className="group"
                >
                  <Link to={`/products/${product.id}`} className="group block">
                    <div className="relative bg-white rounded-[2rem] overflow-hidden shadow-premium hover-lift transition-all duration-500">
                      <div className="aspect-[4/5] overflow-hidden">
                        <img
                          src={getImageUrl(product.image) || "https://images.unsplash.com/photo-1549465220-1a8b9238cd48?auto=format&fit=crop&q=80&w=1000"}
                          className="w-full h-full object-cover transition-transform duration-700 group-hover:scale-110"
                          alt={product.name}
                        />
                        <div className="absolute inset-0 bg-gradient-to-t from-black/40 via-transparent to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300 flex items-center justify-center">
                          <span className="bg-white/20 backdrop-blur-md text-white px-6 py-3 rounded-2xl text-xs font-black uppercase tracking-widest border border-white/20 scale-90 group-hover:scale-100 transition-all duration-500">View Details</span>
                        </div>
                      </div>

                      {/* Badges */}
                      <div className="absolute top-5 left-5 flex flex-col gap-2">
                        {product.badge_text && (
                          <span
                            className="text-[10px] font-black px-3 py-1.5 rounded-full uppercase tracking-widest shadow-lg text-white"
                            style={{ backgroundColor: product.badge_color || 'var(--color-primary)' }}
                          >
                            {product.badge_text}
                          </span>
                        )}
                        {product.customization_config && (
                          <span className="bg-white/90 backdrop-blur-md text-primary text-[10px] font-extrabold px-3 py-1.5 rounded-full uppercase tracking-widest shadow-sm border border-primary/10">
                            Customizable
                          </span>
                        )}
                      </div>

                      <div className="p-8">
                        <p className="text-primary text-[10px] font-black uppercase tracking-[0.2em] mb-3">{product.category_name}</p>
                        <h3 className="text-xl font-bold text-slate-900 mb-4 group-hover:text-primary transition-colors line-clamp-1">{product.name}</h3>
                        <div className="flex justify-between items-center pt-4 border-t border-slate-100">
                          <div className="flex items-center gap-2">
                            <span className="text-2xl font-bold text-slate-900">₹{product.price}</span>
                            {product.discount_price && (
                              <span className="text-sm text-slate-400 line-through">₹{product.discount_price}</span>
                            )}
                          </div>
                          <div className="text-primary-light font-black text-[10px] uppercase tracking-widest">
                            Explore
                          </div>
                        </div>
                      </div>
                    </div>
                  </Link>
                </motion.div>
              ))
            ) : (
              [1, 2, 3, 4].map(n => (
                <div key={n} className="h-[450px] bg-slate-200 animate-pulse rounded-[2rem]"></div>
              ))
            )}
          </div>
        </div>
      </section>

      {/* Why Choose Us */}
      <section className="py-6 md:py-8 bg-white overflow-hidden">
        <div className="container-custom">
          <div className="grid lg:grid-cols-2 gap-10 items-center">
            <motion.div
              initial={{ opacity: 0, x: -50 }}
              whileInView={{ opacity: 1, x: 0 }}
              viewport={{ once: true }}
            >
              <h2 className="text-3xl md:text-4xl font-bold mb-6 leading-tight text-slate-900">
                Why Corporate Leaders <span className="text-primary italic">Trust</span> Soham Gift
              </h2>
              <p className="text-lg text-slate-500 mb-8 leading-relaxed">
                We don't just deliver products; we deliver experiences that reinforce your brand values and appreciation.
              </p>

              <div className="space-y-6">
                {[
                  { title: "Custom Branding", desc: "Advanced printing and engraving technology.", icon: ShieldCheck },
                  { title: "Maharashtra Logistics", desc: "Reliable delivery to all major cities in Maharashtra.", icon: Truck },
                  { title: "Personal Concierge", desc: "A dedicated manager to handle your bulk orders.", icon: Clock },
                ].map((item, idx) => (
                  <div key={idx} className="flex gap-4 group">
                    <div className="flex-shrink-0 w-12 h-12 bg-slate-50 rounded-xl flex items-center justify-center text-primary group-hover:bg-primary group-hover:text-white transition-all duration-300 shadow-sm">
                      <item.icon size={22} />
                    </div>
                    <div>
                      <h4 className="text-xl font-bold text-slate-900 mb-1">{item.title}</h4>
                      <p className="text-slate-600 text-base leading-relaxed">{item.desc}</p>
                    </div>
                  </div>
                ))}
              </div>
            </motion.div>

            <motion.div
              initial={{ opacity: 0, scale: 0.9 }}
              whileInView={{ opacity: 1, scale: 1 }}
              viewport={{ once: true }}
              className="relative flex justify-center lg:justify-end"
            >
              <div className="relative z-10 rounded-[2rem] overflow-hidden shadow-xl max-w-md w-full">
                <img
                  src="https://images.unsplash.com/photo-1522071820081-009f0129c71c?auto=format&fit=crop&q=80&w=1200"
                  alt="Team Collaboration"
                  className="w-full h-full object-cover aspect-square"
                />
              </div>
              {/* Floating elements */}
              <div className="absolute -bottom-4 -left-4 bg-white p-5 rounded-2xl shadow-premium z-20 hidden md:block">
                <p className="text-3xl font-bold text-primary mb-1">98%</p>
                <p className="text-slate-500 font-bold text-[10px] uppercase tracking-widest">Retention Rate</p>
              </div>
              <div className="absolute top-10 -right-5 w-40 h-40 bg-primary/10 rounded-full blur-3xl z-0"></div>
            </motion.div>
          </div>
        </div>
      </section>

      {/* Testimonials */}
      <section className="py-6 md:py-8 bg-slate-900 text-white relative">
        <div className="container-custom">
          <div className="text-center mb-10">
            <span className="text-primary font-black uppercase tracking-[0.3em] text-[10px] mb-3 inline-block">Voices of Trust</span>
            <h2 className="text-3xl md:text-4xl font-bold mb-4">What Corporate Visionaries Say</h2>
            <div className="w-16 h-1 bg-primary mx-auto rounded-full"></div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {testimonials.length > 0 ? (
              testimonials.map((testimonial) => (
                <motion.div
                  key={testimonial.id}
                  whileHover={{ y: -5 }}
                  className="bg-white/5 backdrop-blur-md p-6 rounded-[2rem] border border-white/10 flex flex-col justify-between"
                >
                  <div>
                    <div className="flex gap-1 text-accent mb-6">
                      {[1, 2, 3, 4, 5].map(s => <Star key={s} size={14} fill="currentColor" />)}
                    </div>
                    <p className="text-slate-300 text-base italic mb-8 leading-relaxed font-light">
                      "{testimonial.content}"
                    </p>
                  </div>
                  <div className="flex items-center gap-4 pt-6 border-t border-white/5">
                    <div className="w-12 h-12 bg-primary/20 rounded-xl flex items-center justify-center text-primary font-black text-lg border border-primary/30">
                      {testimonial.name.split(' ').map(n => n[0]).join('').substring(0, 2).toUpperCase()}
                    </div>
                    <div>
                      <h4 className="font-bold text-white text-base">{testimonial.name}</h4>
                      <p className="text-slate-500 text-xs font-medium">{testimonial.role || testimonial.company}</p>
                    </div>
                  </div>
                </motion.div>
              ))
            ) : (
              [1, 2, 3].map((n) => (
                <motion.div
                  key={n}
                  whileHover={{ y: -5 }}
                  className="bg-white/5 backdrop-blur-md p-6 rounded-[2rem] border border-white/10 flex flex-col justify-between"
                >
                  <div>
                    <div className="flex gap-1 text-accent mb-6">
                      {[1, 2, 3, 4, 5].map(s => <Star key={s} size={14} fill="currentColor" />)}
                    </div>
                    <p className="text-slate-300 text-base italic mb-8 leading-relaxed font-light">
                      "The quality of gifts was exceptional, and the branding was perfectly executed. Our employees loved the Diwali hampers! Soham Gift is now our go-to partner."
                    </p>
                  </div>
                  <div className="flex items-center gap-4 pt-6 border-t border-white/5">
                    <div className="w-12 h-12 bg-primary/20 rounded-xl flex items-center justify-center text-primary font-black text-lg border border-primary/30">
                      {n === 1 ? 'RK' : n === 2 ? 'SD' : 'AN'}
                    </div>
                    <div>
                      <h4 className="font-bold text-white text-base">{n === 1 ? 'Rajesh Kumar' : n === 2 ? 'Sneha Desai' : 'Arjun Nair'}</h4>
                      <p className="text-slate-500 text-xs font-medium">{n === 1 ? 'HR Director, Tech Solutions' : 'Procurement Lead, Global Corp'}</p>
                    </div>
                  </div>
                </motion.div>
              ))
            )}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-6 md:py-8 bg-white">
        <div className="container-custom">
          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            whileInView={{ opacity: 1, scale: 1 }}
            viewport={{ once: true }}
            className="relative rounded-[3rem] bg-slate-900 p-10 md:p-16 text-center text-white overflow-hidden shadow-2xl"
          >
            {/* Background Glow */}
            <div className="absolute top-0 left-0 w-full h-full opacity-10 pointer-events-none">
              <div className="absolute -top-1/2 -left-1/4 w-[100%] h-[100%] bg-primary rounded-full blur-[150px]"></div>
              <div className="absolute -bottom-1/2 -right-1/4 w-[100%] h-[100%] bg-blue-600 rounded-full blur-[150px]"></div>
            </div>

            <div className="relative z-10 max-w-3xl mx-auto">
              <Gift className="w-12 h-12 text-primary mx-auto mb-6 animate-bounce" />
              <h2 className="text-3xl md:text-5xl font-bold mb-6 leading-tight">Ready to Elevate Your Gifting Experience?</h2>
              <p className="text-base md:text-lg mb-10 text-slate-300 max-w-xl mx-auto font-light leading-relaxed">
                Join 500+ companies that trust us for their premium corporate requirements. Get a personalized quote within 24 hours.
              </p>
              <div className="flex justify-center">
                <Link to="/products" className="bg-white/10 backdrop-blur-md hover:bg-white/20 text-white font-bold px-16 py-6 rounded-2xl text-xl transition-all border border-white/10">
                  Browse Catalog
                </Link>
              </div>
            </div>
          </motion.div>
        </div>
      </section>
    </div>
  );
};

export default Home;

