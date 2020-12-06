import PageTemplate from '../Template/PageTemplate';
import background from './LoginDesign.svg';
import './LoginPage.css'

const LoginPage = () => {
  return (
    <PageTemplate>
      <img src={background} alt="ppt background" className="loginPage" data-testid="login-page"/>
    </PageTemplate>
  );
}

export default LoginPage