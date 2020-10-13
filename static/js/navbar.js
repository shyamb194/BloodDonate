const menuBtn = document.querySelector(".menu-icon span");
            const loginBtn = document.querySelector(".login-icon");
            const cancelBtn = document.querySelector(".cancel-icon");
            const items = document.querySelector(".nav-items");
            const form = document.querySelector("form");
            menuBtn.onclick = ()=>{
                items.classList.add("active");
                menuBtn.classList.add("hide");
                loginBtn.classList.add("hide");
                cancelBtn.classList.add("show");
            }
            cancelBtn.onclick = ()=>{
                items.classList.remove("active");
                menuBtn.classList.remove("hide");
                loginBtn.classList.remove("hide");
                cancelBtn.classList.remove("show");
                form.classList.remove("active");
                cancelBtn.style.color = "#ff3d00";
            }
            loginBtn.onclick = ()=>{
                form.classList.add("active");
                loginBtn.classList.add("hide");
                cancelBtn.classList.add("show");
            }
            
            
