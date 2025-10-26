import streamlit as st
from PIL import Image

# -----------------------
# Custom Styling
# -----------------------

def local_css():
    st.markdown("""
        <style>
        /* Background */
        .stApp {
            /* CHANGED: Light green gradient */
            background: linear-gradient(120deg, #E8F5E9, #A06CE9);
            font-family: 'Segoe UI', sans-serif;
        }

        /* Title (Login Page) */
        .title {
            text-align: center;
            color: #212121;
            font-size: 2.2em;
            font-weight: bold;
        }
        
        /* Dashboard Welcome Headers */
        .stApp h2 {
             /* CHANGED: Dark green for headers */
            color: #A06CE9;
        }

        /* Cards */
        .card {
            background-color: #ffffff;
            padding: 1.2rem;
            border-radius: 10px;
            box-shadow: 2px 2px 10px rgba(0,0,0,0.1);
            margin-bottom: 1rem;
        }

        /* Sidebar */
        section[data-testid="stSidebar"] {
            /* CHANGED: Dark green sidebar */
            background-color:#AD67F3;
            color: white;
        }

        section[data-testid="stSidebar"] h1, h2, h3, h4, h5 {
            color: white !important;
        }

        /* Buttons */
        div.stButton > button {
             /* CHANGED: Dark green buttons */
            background-color: #4CAF50;
            color: white;
            border-radius: 8px;
            padding: 0.5rem 1rem;
            border: none;
        }
        div.stButton > button:hover {
            /* CHANGED: Darker green on hover */
            background-color: #388E3C;
            color: white;
        }

        /* Metric Boxes */
        .metric-card {
            text-align: center;
            padding: 10px;
             /* CHANGED: Light green metric card */
            background-color: #C8E6C9;
            border-radius: 10px;
            margin: 5px;
        }

        /* Center Image */
        .center {
            display: flex;
            justify-content: center;
        }

        </style>
    """, unsafe_allow_html=True)

# -----------------------
# Pages
# -----------------------

def login_page():
    st.markdown("<div class='title'>♻️ Inorganic Waste & Scrap Management System</div>", unsafe_allow_html=True)
    st.image("https://cdn-icons-png.flaticon.com/512/1048/1048943.png", width=120)
    st.markdown("<br>", unsafe_allow_html=True)

    role = st.selectbox("Select your role:", ["User 👤", "Delivery Man 🚚", "Admin 🛠️"])
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if "User" in role:
            st.session_state['role'] = "User"
        elif "Delivery" in role:
            st.session_state['role'] = "Delivery Man"
        else:
            st.session_state['role'] = "Admin"
        st.session_state['username'] = username
        st.success(f"Welcome, {username}! Redirecting to {st.session_state['role']} dashboard...")
        st.experimental_rerun()

# -----------------------
# USER DASHBOARD
# -----------------------

def user_dashboard():
    st.sidebar.image("https://cdn-icons-png.flaticon.com/512/681/681392.png", width=100)
    st.sidebar.header("User Dashboard")
    page = st.sidebar.radio("Navigate", [
        " Profile Info", " Wastes Sent", " Track Package", " Payment Gateway",
        " About NGOs", " Contact Support", " Feedback"])

    #st.markdown(f"<h2>style=color: black👤 Welcome {st.session_state['username']}</h2>", unsafe_allow_html=True)   
    st.markdown(f"<h2 style='color: black;'>👤 Welcome {st.session_state['username']}</h2>", unsafe_allow_html=True)
    
























    
    from pymongo import MongoClient
    from pymongo.errors import ConnectionFailure, OperationFailure

    # --- 1. CONNECT TO MONGODB ---

    @st.cache_resource
    def get_mongo_client():
        """Establishes a connection to MongoDB."""
        try:
            # Get the connection string from Streamlit secrets
            mongo_uri = st.secrets["MONGO_URI"]
            
            # Create a client
            client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)
            
            # Test the connection
            client.server_info() 
            print("Connected to MongoDB successfully!")
            return client
        
        except KeyError:
            st.error("MONGO_URI not found in Streamlit Secrets. Please add it to .streamlit/secrets.toml")
            return None
        except (ConnectionFailure, OperationFailure) as e:
            st.error(f"Failed to connect to MongoDB: {e}")
            return None

    # Get the client
    client = get_mongo_client()

    # --- 2. SETUP DATABASE AND COLLECTION ---

    # Stop the app if the connection failed
    if client is None:
        st.stop()

    # --- IMPORTANT: Change these names! ---
    # Replace "your_database_name" with your actual database name in Atlas
    db = client["your_database_name"]  
    # Replace "your_collection_name" with the collection you want to store profiles in
    collection = db["user_details_collection"] 
    # ------------------------------------


    # --- 3. YOUR PAGE CODE ---

    # This assumes 'page' is defined earlier in your app
    if page == " Profile Info":
        #st.markdown("<div class='card'><h4>Profile Information</h4>", unsafe_allow_html=True)
        
        # Create the form inputs
        name = st.text_input("Name", placeholder="Enter your full name")
        address = st.text_input("Address", placeholder="123 Green Street")
        contact = st.text_input("Contact", placeholder="9876543210")

        # Change button text to "Save Profile"
        if st.button("Save Profile"):
            # Check if name is provided (as a basic validation)
            if name:
                try:
                    # --- This is the key part ---
                    # Create a dictionary (document) with the data
                    user_document = {
                        "name": name,
                        "address": address,
                        "contact": contact
                    }
                    
                    # Insert the document into your collection
                    result = collection.insert_one(user_document)
                    
                    st.success(f" Profile saved successfully! (ID: {result.inserted_id})")
                    
                except OperationFailure as e:
                    st.error(f"Failed to save data: {e}")
                except Exception as e:
                    st.error(f"An unexpected error occurred: {e}")
            else:
                st.warning("Please enter a name.")

        st.markdown("</div>", unsafe_allow_html=True)












    elif page == " Wastes Sent":
        # --- 1. Define Collection ---
        # This assumes `db` is defined globally in your app (from your connection code)
        try:
            # Use a specific collection for wastes. 
            # MongoDB will create this if it doesn't exist.
            wastes_collection = db["wastes"] 
        except NameError:
            st.error("Database client `db` is not defined. Cannot connect to 'wastes' collection.")
            st.stop()
        except Exception as e:
            st.error(f"Error connecting to 'wastes' collection: {e}")
            st.stop()
            
        # --- 2. Form to Add New Waste ---
        #st.markdown("<div class='card'><h4>Submit New Waste</h4>", unsafe_allow_html=True)
        
        # We need a name to link this waste submission to a user profile
        name = st.text_input("Your Name", placeholder="Enter the name on your profile")
        
        waste_type = st.selectbox(
            "Type of Waste",
            ("Plastic", "Paper", "Glass", "E-waste", "Organic", "Mixed")
        )
        
        quantity = st.text_input("Quantity", placeholder="e.g., 5 kg or 3 items")

        if st.button("Submit Waste"):
            # Basic validation: check that all fields are filled
            if name and waste_type and quantity:
                try:
                    # Create the document to be inserted
                    waste_document = {
                        "submitted_by": name,
                        "type": waste_type,
                        "quantity": quantity,
                        "status": "Pending Pickup" # Automatically set a default status
                    }
                    
                    # Insert the document into your 'wastes' collection
                    result = wastes_collection.insert_one(waste_document)
                    
                    st.success(f"✅ Waste submitted successfully! (ID: {result.inserted_id})")
                    
                except Exception as e:
                    st.error(f"An unexpected error occurred while saving: {e}")
            else:
                st.warning("Please fill in all fields (Name, Type, and Quantity).")
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # --- 3. Display All Wastes Sent ---
        #st.markdown("<hr><div class='card'><h4>List of Wastes Sent</h4>", unsafe_allow_html=True)
        
        try:
            # You need 'import pandas as pd' at the top of your app
            import pandas as pd
            
            # Find all documents in the 'wastes' collection
            # In a real app, you might filter this by user:
            # cursor = wastes_collection.find({"submitted_by": name_from_login})
            cursor = wastes_collection.find()
            wastes_data = list(cursor)
            
            if wastes_data:
                # Convert the data to a pandas DataFrame
                df = pd.DataFrame(wastes_data)
                
                # Reformat columns for a cleaner display
                df.rename(columns={
                    "_id": "Package ID", 
                    "submitted_by": "Submitted By", 
                    "type": "Type", 
                    "quantity": "Quantity", 
                    "status": "Status"
                }, inplace=True)
                
                # Define the order of columns to show
                display_columns = ["Package ID", "Submitted By", "Type", "Quantity", "Status"]
                
                # Use st.dataframe to display the table
                st.dataframe(df[display_columns])
            else:
                st.info("No wastes have been submitted yet.")
                
        except Exception as e:
            st.error(f"Error loading waste data: {e}")
            
        st.markdown("</div>", unsafe_allow_html=True)




















    elif page == " Track Package":
        #st.markdown("<div class='card'><h4>Track Your Package</h4>", unsafe_allow_html=True)
        package_id = st.text_input("Enter Package ID")
        if st.button("Track"):
            st.info(" Status: In Transit")
            st.text(" Delivery Man: Ravi Kumar, ETA: 2 hours")
        st.markdown("</div>", unsafe_allow_html=True)





















    elif page == " Payment Gateway":
        import streamlit.components.v1 as components
        st.markdown("<h3> Payment Gateway</h3>", unsafe_allow_html=True)

        # Read your local HTML file
        with open("the_payment.html", "r") as f:
            html_data = f.read()

        # Render it inside Streamlit
        components.html(html_data, height=600, scrolling=True)























    elif page == " About NGOs":
        #st.markdown("<div class='card'><h4>Our Partner NGOs</h4>", unsafe_allow_html=True)
        st.image("https://cdn-icons-png.flaticon.com/512/3534/3534033.png", width=80)
        
        st.markdown("""
        ###  Green Future Foundation  
        **Mission:** To build a cleaner, greener, and more sustainable future by spreading environmental awareness and driving community-based eco-projects.  
        **Key Initiatives:**  
        - Tree plantation drives across urban and rural India   
        - Renewable energy awareness campaigns  
        - Community composting and waste management programs  
        **Impact:** Over 50,000 trees planted and 200+ local volunteers engaged nationwide.  

        ---
        ###  Clean Planet Trust  
        **Mission:** To create a world free from plastic pollution by promoting recycling, upcycling, and eco-friendly alternatives.  
        **Key Initiatives:**  
        - Plastic waste collection and recycling centers   
        - Beach and city cleanup drives   
        - Educational programs for schools and communities   
        **Impact:** Removed 100+ tons of plastic waste and educated over 10,000 students on sustainable practices.  

        ---
        ###  Rural Empowerment Network  
        **Mission:** Empower rural communities through skill development, sustainable farming, and environmental stewardship.  
        **Key Initiatives:**  
        - Organic farming workshops and farmer training  
        - Water conservation and irrigation efficiency projects   
        - Women’s self-help groups focused on eco-crafts and livelihoods   
        **Impact:** Improved the livelihoods of 1,500+ rural families through sustainable practices.  

        ---
        ###  Blue Earth Foundation  
        **Mission:** To protect marine ecosystems and restore coastal biodiversity.  
        **Key Initiatives:**  
        - Coral reef restoration projects   
        - Coastal mangrove plantation  
        - Ocean cleanup and marine life protection programs   
        **Impact:** Planted 25,000 mangroves and partnered with local fishermen to reduce marine litter by 60%.  

        ---
        ###  Together for Change  
        **Mission:** Build collaborations between citizens, corporates, and NGOs to tackle environmental challenges collectively.  
        **Key Initiatives:**  
        - Sustainable event management and zero-waste campaigns   
        - Climate education through workshops and hackathons  
        - Annual “Eco Fest” celebrating local green innovations  
        **Impact:** Engaged over 100 organizations and 15,000 participants in green collaborations.  
        """)
        
        st.markdown("""
        ---
         *These NGOs are our key partners in promoting sustainability, community awareness, and real-world environmental impact.  
        Together, we believe that every small action leads to a cleaner, greener, and more responsible planet.* 
        """)
        
        st.markdown("</div>", unsafe_allow_html=True)














    





    elif page == " Contact Support": # <-- 1. MAKE SURE this emoji matches your sidebar


        
        from PIL import Image
        from pymongo import MongoClient
        from pymongo.errors import ConnectionFailure, OperationFailure
        import datetime
        from datetime import timezone  # <-- ADD THIS IMPORT

            # --- 1. CONNECT TO MONGODB ---
        client = get_mongo_client()

            # --- 2. SETUP DATABASE AND COLLECTIONS ---
        if client is None:
                st.stop()

            # --- IMPORTANT: Change these names! ---
            # Define your database ONCE
        db = client["your_database_name"] 

            # Define ALL your collections ONCE
        profile_collection = db["user_profiles"]
        feedback_collection = db["user_feedback"]
        support_collection = db["support_tickets"] # <--- DEFINED HERE
            # ------------------------------------

        # This code goes INSIDE your user_dashboard() function

            
        #st.markdown("<div class='card'><h4>Contact Support</h4>", unsafe_allow_html=True)
        msg = st.text_area("Your message")
            
        if st.button("Send Message"):
                if msg:
                    try:
                        # 2. Create the document
                        support_document = {
                            "username": st.session_state['username'], 
                            "message": msg,
                            # 3. Use the correct, safer 'timezone.utc'
                            "timestamp": datetime.datetime.now(timezone.utc), 
                            "status": "New"
                        }
                        
                        # 4. Use the 'support_collection' variable defined at the top
                        result = support_collection.insert_one(support_document)
                        st.success(f"📧 Message sent successfully! (Ticket ID: {result.inserted_id})")
                        
                    except OperationFailure as e:
                        st.error(f"Failed to send message: {e}")
                    except Exception as e:
                        st.error(f"An unexpected error occurred: {e}")
                else:
                    st.warning("Please enter a message.")

        st.markdown("</div>", unsafe_allow_html=True)
















    # This code goes INSIDE your user_dashboard() function

    elif page == " Feedback": # <-- 1. MUST MATCH THE EMOJI in your st.sidebar.radio
        
        
        from datetime import timezone
        # You might have added a variable like this:
        selected_timezone = st.selectbox("Select your timezone", ["IST", "GMT", "EST"], key="user_timezone_select")
        timezone = st.selectbox("Select your timezone", ["IST", "GMT", "EST"], key="admin_timezone_select")
        

        user_timezone = "IST"
        date_string = "some-string"
        # This code will now work:
        # Correct structure
        support_document = {
            "username": st.session_state['username'],
            "message": msg,
            "timestamp": datetime.datetime.now(timezone.utc), # <-- INSIDE the braces
            "status": "New" # <-- INSIDE the braces
        } # <-- The dictionary closes here
        if client is None:
            st.stop()

        db = client["your_database_name"] 
        profile_collection = db["user_profiles"]
        support_collection = db["support_tickets"]
        feedback_collection = db["user_feedback"]
        
        #st.markdown("<div class='card'><h4>Feedback Form</h4>", unsafe_allow_html=True) # Uncommented
        rating = st.slider("Rate our service", 1, 5)
        comments = st.text_area("Comments")
        
        if st.button("Submit Feedback"):
            
            # 2. Add validation (e.g., comments are required)
            if comments:
                try:
                    # 3. Create the document
                    feedback_document = {
                        "username": st.session_state['username'],
                        "rating": rating,
                        "comments": comments,
                        "timestamp": datetime.datetime.now(timezone.utc)
                    }
                    
                    # 4. Insert into the global 'feedback_collection'
                    result = feedback_collection.insert_one(feedback_document)
                    
                    st.success(" Thank you for your valuable feedback!")
                    
                except OperationFailure as e:
                    st.error(f"Failed to submit feedback: {e}")
                except Exception as e:
                    st.error(f"An unexpected error occurred: {e}")
            else:
                # 5. Show a warning if validation fails
                st.warning("Please provide some comments.")

        st.markdown("</div>", unsafe_allow_html=True)











# -----------------------
# DELIVERY MAN DASHBOARD
# -----------------------



def delivery_dashboard():
    st.sidebar.image("https://cdn-icons-png.flaticon.com/512/859/859270.png", width=100)
    st.sidebar.header("Delivery Dashboard")
    page = st.sidebar.radio("Navigate", [
                " Profile & Details", " Assigned Packages", " Update Status", " Route Map", " Notifications"
            ])

    st.markdown(f"<h2 style='color:#1565c0;'> Hello {st.session_state['username']}</h2>", unsafe_allow_html=True)




    

    
    from pymongo import MongoClient
    from pymongo.errors import ConnectionFailure, OperationFailure
    from datetime import timezone
    # --- 1. CONNECT TO MONGODB ---

    @st.cache_resource
    def get_mongo_client():
        """Establishes a connection to MongoDB."""
        try:
            # Get the connection string from Streamlit secrets
            mongo_uri = st.secrets["MONGO_URI"]
            
            # Create a client
            client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)
            
            # Test the connection
            client.server_info() 
            print("Connected to MongoDB successfully!")
            return client
        
        except KeyError:
            st.error("MONGO_URI not found in Streamlit Secrets. Please add it to .streamlit/secrets.toml")
            return None
        except (ConnectionFailure, OperationFailure) as e:
            st.error(f"Failed to connect to MongoDB: {e}")
            return None

    # Get the client
    client = get_mongo_client()

    # --- 2. SETUP DATABASE AND COLLECTION ---

    # Stop the app if the connection failed
    if client is None:
        st.stop()

    # --- IMPORTANT: Change these names! ---
    # Replace "your_database_name" with your actual database name in Atlas
    db = client["your_database_name"]  
    # Replace "your_collection_name" with the collection you want to store profiles in
    collection = db["your_collection_name"] 
    # ------------------------------------







    # This code goes INSIDE your delivery_dashboard() function

    if page == " Profile & Details": # <-- 1. MUST MATCH your sidebar radio string
            db = client["your_database_name"] 

            profile_collection = db["user_profiles"]
            feedback_collection = db["user_feedback"]
            support_collection = db["support_tickets"]

            delivery_profile_collection = db["delivery_profiles"]
            
            #st.markdown("<div class='card'><h4>Profile & Vehicle Info</h4>", unsafe_allow_html=True)
            
            # --- 2. Load existing data for the logged-in delivery man ---
            try:
                current_user = st.session_state['username']
                # Use the new collection
                user_data = delivery_profile_collection.find_one({"username": current_user})
                
                # Set defaults for text inputs
                default_name = user_data.get("name", "") if user_data else "Ravi Kumar"
                default_contact = user_data.get("contact", "") if user_data else "9876543210"
                default_vehicle = user_data.get("vehicle", "") if user_data else "Truck XYZ"
                default_available = user_data.get("available", True) if user_data else True

            except OperationFailure as e:
                st.warning(f"Could not load profile data: {e}")
                default_name, default_contact, default_vehicle, default_available = "Ravi Kumar", "9876543210", "Truck XYZ", True

            # --- 3. Form inputs with defaults ---
            name = st.text_input("Name", value=default_name)
            contact = st.text_input("Contact", value=default_contact)
            vehicle = st.text_input("Vehicle Details", value=default_vehicle)
            available = st.checkbox("Available for delivery", value=default_available)

            # --- 4. Add a button to save the data ---
            if st.button("Update Profile"):
                if name and vehicle: # Basic validation
                    try:
                        # --- 5. Save data using update_one ---
                        query = {"username": st.session_state['username']}
                        new_data = {"$set": {
                            "name": name,
                            "contact": contact,
                            "vehicle": vehicle,
                            "available": available,
                            "username": st.session_state['username'] # Always store the key
                        }}
                        
                        # This updates if exists, or inserts if new (upsert=True)
                        result = delivery_profile_collection.update_one(query, new_data, upsert=True)
                        
                        if result.matched_count > 0 or result.upserted_id:
                            st.success("✅ Profile updated successfully!")
                        
                    except OperationFailure as e:
                        st.error(f"Failed to update profile: {e}")
                else:
                    st.warning("Please enter at least a name and vehicle details.")
                    
            st.markdown("</div>", unsafe_allow_html=True)



















    # This code goes INSIDE your delivery_dashboard() function

    elif page == " Assigned Packages": # <-- 1. MUST MATCH your sidebar radio string
        # --- 2. SETUP DATABASE AND COLLECTIONS ---
        # ... (your other collections) ...
        profile_collection = db["user_profiles"]
        delivery_profile_collection = db["delivery_profiles"] 
        feedback_collection = db["user_feedback"]
        support_collection = db["support_tickets"]

        # --- ADD THIS LINE ---
        packages_collection = db["packages"] 
        # ---------------------

        #st.markdown("<div class='card'><h4>Assigned Packages</h4>", unsafe_allow_html=True) # Uncommented
        
        try:
            # 2. Get the username of the currently logged-in driver
            current_driver = st.session_state['username']
            
            # 3. Find packages assigned to this driver that are NOT yet delivered
            query = {
                "assigned_driver": current_driver,
                "status": {"$ne": "Delivered"}  # $ne means "not equal"
            }
            
            # 4. Fetch the data from the 'packages_collection'
            assigned_packages = list(packages_collection.find(query))
            
            if assigned_packages:
                # 5. Format the data for the table
                display_list = []
                for pkg in assigned_packages:
                    display_list.append({
                        # Use .get() for safety in case a field is missing
                        "Package ID": pkg.get("package_id", "N/A"), 
                        "Type": pkg.get("waste_type", "N/A"),
                        "User Contact": pkg.get("user_contact", "N/A"),
                        "Status": pkg.get("status", "N/A")
                    })
                
                st.table(display_list)
                
            else:
                # 6. Show a message if no packages are found
                st.info("You have no assigned packages at the moment.")
                
        except OperationFailure as e:
            st.error(f"Failed to load packages: {e}")
        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")

        st.markdown("</div>", unsafe_allow_html=True)
    


















    # This code goes INSIDE your delivery_dashboard() function

    elif page == " Update Status": # <-- 1. MUST MATCH your sidebar radio string
       


        #st.markdown("<div class='card'><h4>Update Package Status</h4>", unsafe_allow_html=True) # Uncommented
        
        package_id = st.text_input("Package ID")
        status = st.selectbox("Select Status", ["Collected", "In Transit", "Delivered"])
        notes = st.text_area("Notes (optional)")
        
        if st.button("Update Status"):
            
            # 2. Validate that a Package ID was entered
            if package_id:
                try:
                    # 3. Define the package to find
                    query = {"package_id": package_id} 
                    # Note: If your package_id is an integer, use:
                    # query = {"package_id": int(package_id)}
                    
                    # 4. Define the data to change
                    new_data = {"$set": {
                        "status": status,
                        "notes": notes,
                        "last_updated": datetime.datetime.now(timezone.utc)
                    }}
                    
                    # 5. Update the document in the 'packages_collection'
                    result = packages_collection.update_one(query, new_data)
                    
                    # 6. Check if the update was successful
                    if result.matched_count > 0:
                        st.success(f"✅ Package {package_id} updated to {status}")
                    else:
                        st.warning(f"⚠️ No package found with ID: {package_id}")
                        
                except OperationFailure as e:
                    st.error(f"Failed to update status: {e}")
                except Exception as e:
                    st.error(f"An unexpected error occurred: {e}")
            else:
                st.warning("Please enter a Package ID.")

        st.markdown("</div>", unsafe_allow_html=True)




























    elif page == " Route Map":
        st.info(" Route optimization map feature coming soon!")

    # This code goes INSIDE your delivery_dashboard() function





















    elif page == " Notifications": # <-- 1. MUST MATCH your sidebar radio string

        st.markdown("<div class='card'><h4>Notifications</h4>", unsafe_allow_html=True) # Uncommented
        
        try:
            # 2. Get the username of the currently logged-in driver
            current_driver = st.session_state['username']
            
            # 3. Define the query to find new, un-actioned jobs
            # We assume a 'Pending Pickup' status is set by the admin
            query = {
                "assigned_driver": current_driver,
                "status": "Pending Pickup" 
            }
            
            # 4. Fetch all new notifications from 'packages_collection'
            new_notifications = list(packages_collection.find(query))
            
            if not new_notifications:
                # 5. Show a message if there are no new jobs
                st.info("No new notifications.")
            else:
                # 6. Loop through and display each new job
                st.write("You have new pickup assignments:")
                for pkg in new_notifications:
                    # Use .get() for safety, in case a field is missing
                    pkg_id = pkg.get("package_id", "N/A")
                    location = pkg.get("pickup_location", "N/A")
                    
                    # Display the notification
                    st.success(f"🔔 New Pickup Assigned: Package #{pkg_id} - Location: {location}")
                    
        except OperationFailure as e:
            st.error(f"Failed to load notifications: {e}")
        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")

        st.markdown("</div>", unsafe_allow_html=True)


















# -----------------------
# ADMIN DASHBOARD
# -----------------------

def admin_dashboard():
    st.sidebar.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=100)
    st.sidebar.header("Admin Dashboard")
    page = st.sidebar.radio("Navigate", [
        " Dashboard", " Manage Users", " Manage Delivery", " Manage Packages",
        " Manage NGOs", " Reports", " Notifications", " Feedback Management"
    ])


    

    
    from pymongo import MongoClient
    from pymongo.errors import ConnectionFailure, OperationFailure

    # --- 1. CONNECT TO MONGODB ---

    @st.cache_resource
    def get_mongo_client():
        """Establishes a connection to MongoDB."""
        try:
            # Get the connection string from Streamlit secrets
            mongo_uri = st.secrets["MONGO_URI"]
            
            # Create a client
            client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000)
            
            # Test the connection
            client.server_info() 
            print("Connected to MongoDB successfully!")
            return client
        
        except KeyError:
            st.error("MONGO_URI not found in Streamlit Secrets. Please add it to .streamlit/secrets.toml")
            return None
        except (ConnectionFailure, OperationFailure) as e:
            st.error(f"Failed to connect to MongoDB: {e}")
            return None

    # Get the client
    client = get_mongo_client()

    # --- 2. SETUP DATABASE AND COLLECTION ---

    # Stop the app if the connection failed














    


        # --- 2. SETUP DATABASE AND COLLECTIONS ---
    if client is None:
        st.error("Database connection failed. App cannot start.")
        st.stop()

    # --- Define ALL your collections here, in the global scope ---
    db = client["your_database_name"] 
    profile_collection = db["user_profiles"]
    delivery_profile_collection = db["delivery_profiles"]
    packages_collection = db["packages"]
    feedback_collection = db["user_feedback"]
    support_collection = db["support_tickets"]

    # ------------------------------------
    if page == " Dashboard":
        try:
            # 1. Get counts from your collections
            user_count = profile_collection.count_documents({})
            delivery_count = delivery_profile_collection.count_documents({})
            pending_count = packages_collection.count_documents({"status": "Pending Pickup"})
            # Note: Donations are still static as we don't have a collection for it
            
            # 2. Display metrics (This fixes your column layout)
            col1, col2, col3, col4 = st.columns(4)
            with col1: 
                st.metric("Total Users", user_count)
            with col2: 
                st.metric("Delivery Staff", delivery_count)
            with col3: 
                st.metric("Pending Jobs", pending_count)
            with col4: 
                st.metric("Donations (₹)", "8,000") # This is still static
        
        except OperationFailure as e:
            st.error(f"Failed to load metrics: {e}")

    # --- [NEW] Manage Users Page ---
    elif page == " Manage Users":
        st.subheader("User Account Management")
        try:
            # Find all documents in the 'profile_collection'
            all_users = list(profile_collection.find({}, {"_id": 0})) # {"_id": 0} hides the complex Mongo ID
            if all_users:
                st.dataframe(all_users, use_container_width=True)
            else:
                st.info("No users found.")
        except OperationFailure as e:
            st.error(f"Failed to load users: {e}")

    # --- [NEW] Manage Delivery Page ---
    elif page == " Manage Delivery":
        st.subheader("Delivery Staff Management")
        try:
            # Find all documents in the 'delivery_profile_collection'
            all_drivers = list(delivery_profile_collection.find({}, {"_id": 0}))
            if all_drivers:
                st.dataframe(all_drivers, use_container_width=True)
            else:
                st.info("No delivery staff found.")
        except OperationFailure as e:
            st.error(f"Failed to load delivery staff: {e}")
        # --- Add new driver form (Example) ---
        st.markdown("---")
        st.subheader("Add New Delivery Staff")
        # You can add st.text_input and a button here to insert into 'delivery_profile_collection'

    # --- [NEW] Manage Packages Page ---
    elif page == " Manage Packages":
        st.subheader("Package & Collection Management")
        try:
            # Find all documents in the 'packages_collection'
            all_packages = list(packages_collection.find({}, {"_id": 0}))
            if all_packages:
                st.dataframe(all_packages, use_container_width=True)
            else:
                st.info("No packages found.")
        except OperationFailure as e:
            st.error(f"Failed to load packages: {e}")

    elif page == " Manage NGOs":
        st.info("Add/edit NGOs and verify details.")

    elif page == " Reports":
        st.info("Generate analytics and reports on operations.")

    elif page == " Notifications":
        st.success("Send system updates to users and delivery men.")

    # --- [NEW] Feedback Management Page ---
    elif page == " Feedback Management":
        st.subheader("User Feedback")
        try:
            # Find all documents in the 'feedback_collection'
            all_feedback = list(feedback_collection.find({}, {"_id": 0}))
            if all_feedback:
                st.dataframe(all_feedback, use_container_width=True)
            else:
                st.info("No feedback submitted yet.")
        except OperationFailure as e:
            st.error(f"Failed to load feedback: {e}")


















    # This code goes INSIDE your admin_dashboard() function

    elif page == " Manage Users": # <-- 1. MUST MATCH your sidebar radio string
        
        st.subheader("User Account Management")
        
        try:
            # 2. Find all documents in the 'profile_collection'
            #    {"_id": 0} hides the complex MongoDB ObjectId column
            all_users = list(profile_collection.find({}, {"_id": 0})) 
            
            if all_users:
                # 3. Display the data in an interactive table
                st.dataframe(all_users, use_container_width=True)
            else:
                st.info("No users found in the database.")
                
        except OperationFailure as e:
            st.error(f"Failed to load users: {e}")
        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")





















    elif page == " Manage Delivery":
        st.info("Assign packages and manage delivery team.")

    # This code goes INSIDE your admin_dashboard() function

    elif page == "📦 Manage Packages": # <-- 1. MUST MATCH your sidebar radio string
        
        st.subheader("All Waste Collections & Package Statuses")
        
        try:
            # 2. Find all documents in the 'packages_collection'
            #    {"_id": 0} hides the complex MongoDB ObjectId column
            all_packages = list(packages_collection.find({}, {"_id": 0})) 
            
            if all_packages:
                # 3. Display the data in an interactive table
                st.dataframe(all_packages, use_container_width=True)
            else:
                st.info("No packages found in the database.")
                
        except OperationFailure as e:
            st.error(f"Failed to load packages: {e}")
        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")

















    elif page == " Manage NGOs":
        st.info("Add/edit NGOs and verify details.")

    elif page == " Reports":
        st.info("Generate analytics and reports on operations.")

    # This code goes INSIDE your admin_dashboard() function
















    elif page == " Notifications": # <-- 1. MUST MATCH your sidebar radio string
        
        st.subheader("New Support Tickets")
        try:
            # 2. Find all documents in 'support_collection' with status "New"
            new_tickets = list(support_collection.find(
                {"status": "New"}, 
                {"_id": 0} # Hide the Mongo ID
            ))
            
            if new_tickets:
                st.warning("You have new support tickets to review:")
                st.dataframe(new_tickets, use_container_width=True)
            else:
                st.info("No new support tickets.")
                
        except OperationFailure as e:
            st.error(f"Failed to load support tickets: {e}")
        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")

        st.markdown("---")
        st.subheader("Recent User Feedback")
        try:
            # 3. Find the 10 most recent feedback items
            # We sort by 'timestamp' in descending order (-1) and limit to 10
            recent_feedback = list(feedback_collection.find(
                {}, 
                {"_id": 0}
            ).sort("timestamp", -1).limit(10)) 
            
            if recent_feedback:
                st.write("Showing the 10 most recent feedback submissions:")
                st.dataframe(recent_feedback, use_container_width=True)
            else:
                st.info("No feedback submitted yet.")
                
        except OperationFailure as e:
            st.error(f"Failed to load feedback: {e}")
        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")

    elif page == " Feedback Management": # <-- 1. MUST MATCH your sidebar radio string
        
        st.subheader("All User Feedback and Ratings")
        
        try:
            # 2. Find all documents in the 'feedback_collection'
            #    We sort by timestamp (-1) to show the newest feedback first
            all_feedback = list(feedback_collection.find({}, {"_id": 0}).sort("timestamp", -1)) 
            
            if all_feedback:
                # 3. Display all feedback in an interactive table
                st.dataframe(all_feedback, use_container_width=True)
            else:
                st.info("No feedback has been submitted yet.")
                
        except OperationFailure as e:
            st.error(f"Failed to load feedback: {e}")
        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")

# -----------------------
# Main App
# -----------------------

def main():
    local_css()

    if 'role' not in st.session_state:
        st.session_state['role'] = None

    if st.session_state['role'] is None:
        login_page()
    else:
        if st.session_state['role'] == "User":
            user_dashboard()
        elif st.session_state['role'] == "Delivery Man":
            delivery_dashboard()
        elif st.session_state['role'] == "Admin":
            admin_dashboard()



        st.sidebar.markdown("---")
        if st.sidebar.button("🔒 Logout"):
            st.session_state['role'] = None
            st.session_state['username'] = None
            st.rerun() # <-- FIX

if __name__ == "__main__":
    main()
